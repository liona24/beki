from flask import current_app, jsonify
import cv2 as cv
import exifread
import dateutil

import os
import numpy as np
import hashlib
from io import BytesIO
import datetime

import database

db = database.db


def _get_created_timestamp(buf):
    copy = BytesIO(buf)
    tags = exifread.process_file(copy)

    stamps = []

    for k in tags:
        if "datetime" in k.lower():
            try:
                dt = dateutil.parser.parse(tags[k])
            except ValueError:
                continue

            stamps.append(int(dt.timestamp()))

    if len(stamps) == 0:
        stamps.append(int(datetime.datetime.utcnow().timestamp()))

    stamp = min(stamps)
    return stamp


def _read_file(file):
    in_buf = file.read()

    stamp = _get_created_timestamp(in_buf)

    in_buf = np.asarray(bytearray(in_buf), dtype=np.uint8)
    img = cv.imdecode(in_buf, cv.IMREAD_COLOR)

    return img, stamp


def _store_unified(img, timestamp):
    w, h = current_app.config["IMG_CROP_SIZE"]
    assert w != h, "TODO we might want to actually crop the image"

    # invert if not landscape
    if img.shape[0] > img.shape[1]:
        w, h = h, w

    img = cv.resize(img, (w, h), interpolation=cv.INTER_AREA)

    _, out_buf = cv.imencode(".png", img)
    out_buf = bytes(out_buf)
    h = hashlib.sha1()
    h.update(out_buf)
    file_name = h.hexdigest() + ".png"

    dst_path = os.path.join(current_app.config["IMG_UPLOAD_PATH"], file_name)
    if not os.path.exists(dst_path):

        with open(dst_path, "wb") as f:
            f.write(out_buf)

        meta = database.ImageMeta(
            picture=file_name,
            timestamp=timestamp
        )
        db.session.add(meta)
        db.session.commit()

    return file_name


def _preprocess(imagepath):
    pass


def upload_img_file(file):
    img_with_meta = _read_file(file)
    if img_with_meta is None:
        return None

    return _store_unified(*img_with_meta)


def find_composition(images):
    pass
    # important: Add titles to images
    # suggest a structure based on either an old facility protocol or on best effort time clustering


def find_composition_with_ref(images, protocol):
        old_titles = []
        old_structure = []
        for entry in protocol.entries:
            old_titles.append(entry.title)
            old_structure.append(list(map(lambda f: (f.title, f.picture), entry.flaws)))
    pass
    # important: Add titles to images
    # suggest a structure based on either an old facility protocol or on best effort time clustering


def preprocess(image_name):
    meta = db.session.query(database.ImageMeta.id)\
        .filter(database.ImageMeta.picture == image_name)\
        .scalar()

    if meta is None:
        return 404

    path = os.path.join(current_app.config["IMAGE_UPLOAD_DIR"], image_name)
    if not os.path.exists(path):
        db.session.delete(meta)
        db.session.commit()
        return 404

    if meta.data:
        return None

    data = _preprocess(path)

    if data is None:
        return 500

    meta.data = data
    db.session.commit()

    return None
