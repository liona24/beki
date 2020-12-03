import os
import hashlib

from flask import Flask, request, jsonify, abort, send_from_directory
from werkzeug.utils import secure_filename
from sqlalchemy import or_, and_
import cv2 as cv
import numpy as np

import database
from post import api_post
from tex import render_protocol, configure_jinja
from img import upload_img_file

app = Flask(__name__)

DB_PATH = "/tmp/beki.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_PATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["IMG_UPLOAD_PATH"] = "/tmp/beki/uploads"
app.config["IMG_CROP_SIZE"] = (342, 256)

app.config["TEX_WORKDIR"] = "/tmp/beki/tex"

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
        results[file.name] = upload_img_file(file)

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


@app.route("/api/_render/<int:id>", methods=["GET"])
def render(id):
    protocol = db.session.query(database.Protocol)\
        .filter(database.Protocol.id == id)\
        .first_or_404()

    return render_protocol(protocol.serialize(full=True))


if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)
