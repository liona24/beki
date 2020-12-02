import os
import hashlib

from flask import Flask, request, jsonify, abort, send_from_directory
from werkzeug.utils import secure_filename
from sqlalchemy import or_
import cv2 as cv
import numpy as np

import database
from post import api_post
from tex import render_protocol, configure_jinja

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


def int_or_400(string):
    try:
        rv = int(string)
    except ValueError:
        abort(400)

    return rv


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
    like_query = f"%{query}%"

    query_builder = db.session.query(table)
    columns = [ (table, name) for name in table.discoverable ]
    conditions = []
    i = 0
    while i < len(columns):
        table, name = columns[i]
        if type(name) == str:
            conditions.append(get_column(table, name).like(like_query))
        else:
            # name is actually another table reference
            table = name
            columns.extend([ (table, name) for name in table.discoverable ])
            query_builder = query_builder.join(table)

        i += 1

    result = query_builder\
        .filter(or_(*conditions))\
        .distinct()\
        .limit(10)\
        .all()

    return jsonify(list(map(lambda record: record.serialize(), result)))


def allowed_file(file):
    # i suppose this does not even matter since we are processing the images
    # before doing anything with them  opencv will surely revolt if the
    # files are no valid images
    return True


def process_image(file):
    in_buf = file.read()
    in_buf = np.asarray(bytearray(in_buf), dtype=np.uint8)
    img = cv.imdecode(in_buf, cv.IMREAD_COLOR)
    if img is None:
        return None

    w, h = app.config["IMG_CROP_SIZE"]
    assert w != h, "TODO we might want to actually crop the image"
    img = cv.resize(img, (w, h), interpolation=cv.INTER_AREA)

    _, out_buf = cv.imencode(".png", img)
    out_buf = bytes(out_buf)
    h = hashlib.sha1()
    h.update(out_buf)
    file_name = h.hexdigest() + ".png"

    dst_path = os.path.join(app.config["IMG_UPLOAD_PATH"], file_name)
    if not os.path.exists(dst_path):
        # TODO: Feature extraction
        # Some keywords which might be useful:
        # - GrabCut
        # - ORB
        # - Unsupervised learning of foreground object detection
        # - locality sensitive hashing
        #       https://github.com/RSIA-LIESMARS-WHU/LSHBOX
        #       https://github.com/kayzhu/LSHash/blob/master/lshash/lshash.py
        #       https://github.com/spotify/annoy
        #       https://medium.com/machine-learning-world/feature-extraction-and-similar-image-search-with-opencv-for-newbies-3c59796bf774


        orb = cv.ORB_create()
        mask = None
        keypoints, descriptors = orb.detectAndCompute(img, mask)
        # 2 modes: Full for facility images and masked (i.e. obj of interest only)
        # for all other images

        with open(dst_path, "wb") as f:
            f.write(out_buf)

    return file_name


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
        results[file.name] = process_image(file)

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
