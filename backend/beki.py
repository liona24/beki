import os
import hashlib
import binascii
from itertools import chain

from flask import Flask, request, jsonify, abort, send_from_directory, json
from werkzeug.utils import secure_filename
from sqlalchemy import or_, and_
import cv2 as cv
import numpy as np

import database
from post import api_post
from tex import render_protocol, configure_jinja
import img

app = Flask(__name__)
app.config.from_object("settings")
app.config.from_envvar("BEKI_SETTINGS", silent=True)

database.init_db(app)
configure_jinja(app)
db = database.db

if not os.path.exists(app.config["IMG_UPLOAD_PATH"]):
    os.makedirs(app.config["IMG_UPLOAD_PATH"])


def param_or_400(name):
    rv = request.json.get(name, None)
    if rv is None:
        abort(400)
    return rv


def escape_for_like_query(query):
    return query.replace("%", r"\%")


def get_column(table, name):
    return table.__table__.columns[name]


def generic_autocomplete_handler(table, key, query):
    if key not in table.autocompleteable:
        abort(404)

    query = escape_for_like_query(query)

    column = get_column(table, key)
    result = db.session.query(column)\
        .filter(column.like(f"%{query}%"))\
        .distinct()\
        .limit(10)\
        .all()

    return jsonify(list(map(lambda record: record[0], result)))


def generic_discover_handler(table, query):
    if len(table.discoverable) == 0:
        abort(404)

    query = escape_for_like_query(query)
    keyword_queries = [ f"%{part}%" for part in filter(None, query.split(" ")) ]
    if len(keyword_queries) == 0:
        return jsonify([])

    query_builder = db.session.query(table)
    columns = [ (table, name) for name in table.discoverable ]
    conditions = [ [] for _ in range(len(keyword_queries)) ]
    i = 0
    while i < len(columns):
        table, name = columns[i]
        if type(name) == str:
            for cond, kw in zip(conditions, keyword_queries):
                cond.append(get_column(table, name).like(kw))
        else:
            # name is actually another table reference
            table = name
            columns.extend([ (table, name) for name in table.discoverable ])
            query_builder = query_builder.join(table)

        i += 1

    # each keyword has to be present, no matter where
    conditions = map(lambda x: or_(*x), conditions)
    conditions = and_(*conditions)

    result = query_builder\
        .filter(conditions)\
        .distinct()\
        .limit(10)\
        .all()

    return jsonify(list(map(lambda record: record.serialize(), result)))


def allowed_file(file):
    # i suppose this does not even matter since we are processing the images
    # before doing anything with them  opencv will surely revolt if the
    # files are no valid images
    return True


@app.route("/api/_autocomplete", methods=["GET", "POST"])
def autocomplete():
    query = param_or_400("q")
    if len(query) < 1:
        abort(400)

    data_src = param_or_400("src")
    key = param_or_400("key")

    table = database.TABLES.get(data_src, None)
    if table is None:
        abort(404)

    return generic_autocomplete_handler(table, key, query)


@app.route("/api/_discover", methods=["GET", "POST"])
def discover():
    query = param_or_400("q")
    if len(query) < 1:
        abort(400)

    data_src = param_or_400("src")

    table = database.TABLES.get(data_src, None)
    if table is None:
        abort(404)

    return generic_discover_handler(table, query)


@app.route("/api/_upload", methods=["POST"])
def upload_image():
    files = []
    for key in request.files:
        file = request.files[key]
        if not allowed_file(file):
            abort(400)

        files.append(file)

    results = {}
    for file in files:
        results[file.name] = img.upload_img_file(file)

    if len(results) == 1:
        # initialize preprocessing for single file uploads automatically
        for res in results.values():
            img.preprocess(res)

    return jsonify(results)


@app.route("/api/<collection>/<int:id>", methods=["GET"], defaults={'recursive': False})
@app.route("/api/<collection>/<int:id>/recursive", methods=["GET"], defaults={'recursive': True})
def api_get(collection, id, recursive):
    table = database.TABLES.get(collection, None)
    if table is None:
        abort(404)

    result = db.session.query(table)\
        .filter(getattr(table, "id") == id)\
        .first_or_404()

    return jsonify(result.serialize(full=recursive))


api_post = app.route("/api/<collection>", methods=["POST"])(api_post)


@app.route("/images/<img>", methods=["GET"])
def serve_img(img):
    img_path = secure_filename(img)
    return send_from_directory(app.config["IMG_UPLOAD_PATH"], img_path)


@app.route("/api/_display_render/<file>", methods=["GET"])
def display(file):
    key = secure_filename(file) + ".pdf"

    path = os.path.join(app.config["RENDER_SERVE_PATH"], key)
    if not os.path.exists(path):
        abort(404)

    def read_pdf():
        with open(path, 'rb') as f:
            yield from f

        os.remove(path)

    resp = app.response_class(read_pdf(), mimetype="application/pdf")
    resp.headers.set("Content-Disposition", "attachment", filename=key)
    return resp


@app.route("/api/_render/<int:id>", methods=["GET"])
def render(id):
    protocol = db.session.query(database.Protocol)\
        .filter(database.Protocol.id == id)\
        .first_or_404()

    return render_protocol(protocol.serialize(full=True))


@app.route("/api/_render/<int:id>/legacy", methods=["GET"])
def render_legacy(id):
    protocol = db.session.query(database.LegacyProtocol)\
        .filter(database.LegacyProtocol.id == id)\
        .first_or_404()

    protocol = json.loads(protocol.data)

    return render_protocol(protocol)


@app.route("/api/_render", methods=["POST"])
def render_raw():
    b64 = request.json.get("data", None)
    if b64 is None:
        abort(400)

    try:
        protocol = binascii.a2b_base64(b64)
        protocol = protocol.decode("raw_unicode_escape")
        protocol = json.loads(protocol)
    except (binascii.Error, json.JSONDecodeError):
        abort(400)

    try:
        resp = render_protocol(protocol, raw=True)
    except:
        return jsonify(err="Da fehlen wohl noch ein paar Dinge :(")
    else:
        return resp


@app.route("/api/_imaging/preprocess", methods=["POST"])
def preprocess():
    images = param_or_400("images")

    if not isinstance(images, list) or len(images) == 0:
        abort(400)

    errors = []

    for i in images:
        err = img.preprocess(i)
        if err is not None:
            errors.append({ i: err })

    return jsonify(errors=errors)


@app.route("/api/_wizard/autocompose", methods=["POST"])
def wizard_autocompose():
    images = param_or_400("images")

    if not isinstance(images, list) or len(images) == 0:
        abort(400)

    facility_id = request.json.get("facility", None)
    protocol = None
    if facility_id is not None:
        try:
            facility_id = int(facility_id)
        except ValueError:
            abort(400)

        protocol = db.session.query(database.Protocol)\
            .filter(database.Protocol.facility_id == facility_id)\
            .scalar()

    if protocol is not None:
        comp = img.find_composition_with_ref(images, protocol)
    else:
        comp = img.find_composition(images)

    return jsonify(comp)


@app.route("/api/_wizard/assemble", methods=["POST"])
def wizard_assemble():
    entries = param_or_400("entries")

    if not isinstance(entries, list):
        abort(400)

    facility_id = param_or_400("facility")
    try:
        facility_id = int(facility_id)
    except ValueError:
        abort(400)

    facility = db.session.query(database.Facility)\
        .filter(database.Facility.id == facility_id)\
        .first_or_404()

    protocol = db.session.query(database.Protocol)\
        .filter(database.Protocol.facility_id == facility_id)\
        .scalar()

        def prep_entry(e):
            e.pop("id", None)
            flaws = e.get("flaws", [])

            e["flaws"] = list(map(lambda pic: dict(picture=pic), flaws))
            return e

        entries = list(map(prep_entry, entries))

    if protocol is None:
        blueprint = dict(facility=facility.serialize(full=True), entries=entries)
    else:
        def edit_dist(s0, s1):
            diff = abs(len(s0) - len(s1))
            for c0, c1 in zip(s0, s1):
                diff += int(c0 != c1)
            return diff

        meta_keys = [ "$status", "$type", "$repr", "id" ]

        for entry in entries:
            title = entry.get("title", None)

            if not title:
                continue

            best = (3, None)
            for ref in protocol.entries:
                ed = edit_dist(ref.title, title)
                if ed < best[0]:
                    best = ed, ref

            if best[1] is None:
                continue

            updates = best[1].serialize('no_secondary')

            if len(entry["flaws"]) == 1 and len(ref.flaws) == 1:
                flaw = ref.flaws[0].serialize()
                for key in meta_keys:
                    flaw.pop(key, None)
                flaw.pop("picture", None)
                entry["flaws"][0].update(flaw)

            for key in  chain(meta_keys, [ "title", "flaws" ]):
                updates.pop(key, None)
            entry.update(updates)

        protocol = protocol.serialize('no_secondary')
        for key in chain(meta_keys, [ "entries", "inspection_date" ]):
            protocol.pop(key, None)

        blueprint = protocol
        blueprint["entries"] = entries

    return jsonify(blueprint)


if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)
