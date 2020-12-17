from flask import current_app, jsonify, json
import cv2 as cv
import exifread
import dateutil.parser
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import AffinityPropagation

import os
import numpy as np
import hashlib
from io import BytesIO
import datetime
from collections import defaultdict

import database

db = database.db


def _get_created_timestamp(buf):
    copy = BytesIO(buf)
    tags = exifread.process_file(copy)

    stamps = []

    for k in tags:
        if "datetime" in k.lower():
            try:
                dt = dateutil.parser.parse(str(tags[k]))
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
    im = cv.imread(imagepath, cv.IMREAD_COLOR)

    if im is None:
        return None

    orb = cv.ORB_create(100)
    _, desc = orb.detectAndCompute(im, None)

    def as_hex(d):
        return bytes(d).hex()

    features = json.dumps(list(map(as_hex, desc)), separators=(',', ':'))
    return features


def upload_img_file(file):
    img_with_meta = _read_file(file)
    if img_with_meta is None:
        return None

    return _store_unified(*img_with_meta)


def _get_features(picture):
    features = db.session.query(database.ImageMeta.features)\
        .filter(database.ImageMeta.picture == picture)\
        .scalar()
    if not features:
        return None

    hex_features = json.loads(features)

    def parse_hex(f):
        return list(bytes.fromhex(f))

    features = np.array(list(map(parse_hex, hex_features)), np.uint8)
    return features


def find_composition(images):
    # this one is simple right now: Cluster images based on the time they were
    # taken. The expected scenario is that images, which are related are taken
    # at a somewhat similiar time.

    meta = []
    for i, im in enumerate(images):
        ts = db.session.query(database.ImageMeta.timestamp)\
            .filter(database.ImageMeta.picture == im)\
            .scalar()

        if ts is not None:
            meta.append((ts, i))

    entries = []

    stamps = [ [m[0]] for m in meta ]
    stamps = np.array(stamps)
    stamps -= stamps.min()
    mx = stamps.max()
    if mx > np.finfo(np.float32).eps:
        stamps = np.divide(stamps, mx)

        ap = AffinityPropagation(random_state=101010101)
        y = ap.fit_predict(stamps)

        clusters = { i: [] for i in y }

        for im_i, cluster_i in enumerate(y):
            clusters[cluster_i].append(meta[im_i])

        ordered = sorted(clusters.values(), key=lambda c: min(c))
        for cluster in ordered:
            ims = list(map(lambda m: images[m[1]], cluster))
            entries.append({
                "id": None,
                "flaws": ims
            })
    else:
        for _, i in meta:
            entries.append({
                "id": None,
                "flaws": [ images[i] ]
            })

    return entries


def find_composition_with_ref(images, protocol):
    ref = []
    for i, entry in enumerate(protocol.entries):
        title = entry.title
        ims = []
        for flaw in entry.flaws:
            pic = flaw.picture
            if not pic:
                continue

            features = _get_features(pic)
            if features is not None:
                ref.append((features, i))

    new = []
    for im in images:
        f = _get_features(im)
        if f is not None:
            new.append((f, im))

    # Step 1: Match against all the existing clusters of pictures
    # and report the cluster (entry) with the highest score
    bf = cv.BFMatcher(cv.NORM_HAMMING, True)
    best_matches = defaultdict(list)
    for new_f, new_im in new:
        best = (0.2, -1)  # only respect correspondences where at least 20% of features match
        for ref_f, entry_i in ref:
            matches = bf.knnMatch(new_f, ref_f, k=1)
            count = sum(map(len, matches))
            sim = count / min(len(new_f), len(ref_f))
            if sim > best[0]:
                best = (sim, entry_i)

        best_matches[best[1]].append((best[0], new_im))

    # Step 2: Aggregate similiar matching images into the corresponding new entries
    entries = []
    outliers = list(map(lambda m: m[1], best_matches[-1]))
    for i in best_matches:
        if i == -1:
            continue

        matches = best_matches[i]

        if len(matches) == 1:
            im = matches[0][1]
            entries.append({
                "id": protocol.entries[i].id,
                "flaws": [ im ]
            })
        else:
            # possibly detect outliers
            lof = LocalOutlierFactor(n_neighbors=min(len(matches), 5))
            sims = np.array(list(map(lambda m: [ m[0] ], matches)))
            labels = lof.fit_predict(sims)

            # determine whether the "outlier" is actually our best match and
            # the rest is crap
            neg = labels < 0
            if neg.any():
                pos = labels > 0
                out_label = np.sign(sims[pos == True].mean() - sims[neg == True].mean())
            else:
                out_label = 1

            flaws = []
            for (_, im), label in zip(matches, labels):
                if label * out_label > 0:
                    flaws.append(im)
                else:
                    outliers.append(im)
            entries.append({
                "id": protocol.entries[i].id,
                "flaws": flaws
            })

    # Step 3: Try to cluster outliers together
    for im in outliers:
        # lulz
        entries.append({
            "id": None,
            "flaws": [ im ]
        })

    return entries


def preprocess(image_name):
    meta = db.session.query(database.ImageMeta)\
        .filter(database.ImageMeta.picture == image_name)\
        .scalar()

    if meta is None:
        return 404

    path = os.path.join(current_app.config["IMG_UPLOAD_PATH"], image_name)
    if not os.path.exists(path):
        db.session.delete(meta)
        db.session.commit()
        return 404

    if meta.features:
        return None

    features = _preprocess(path)

    if features is None:
        return 500

    meta.features = features
    db.session.commit()

    return None
