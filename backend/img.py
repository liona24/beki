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
    old_comp = []
    for entry in protocol.entries:
        title = entry.title
        ims = []
        for flaw in entry.flaws:
            pic = flaw.picture
            if not pic:
                continue

            features = _get_features(pic)
            if features:
                ims.append(features)

        old_comp.append((ims, entry))

    indices = []
    new_features = []
    for i, im in enumerate(images):
        f = _get_features(im)
        if f:
            indices.append(i)
            new_features.append(f)

    # Step 1: Match against all the existing clusters of pictures
    # and report the cluster (entry) with the highest score
    bf = cv.BFMatcher(cv.NORM_HAMMING, True)
    best_matches = defaultdict(list)
    for ni, nf in enumerate(new_features):
        best_sim = 0.2
        best_match = -1
        for mi, (member_features, _) in enumerate(old_comp):
            metrics = []
            for mf in member_features:
                matches = bf.knnMatch(mf, nf, k=1)
                count = 0
                for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        count += 1
                metrices.append(count / min(len(mf), len(nf)))

            sim = np.array(metrics).mean()
            if sim > best_sim:
                best_sim = sim
                best_match = mi

        best_matches[best_match].append((best_sim, ni))

    # Step 2: Aggregate similiar matching images into the corresponding new entries
    entries = []
    outliers = list(map(lambda m: m[1], best_matches[-1]))
    for mi in range(len(old_comp)):
        matches = best_matches[mi]
        if len(matches) == 0:
            continue

        if len(matches) == 1:
            ni = matches[0][1]
            im_i = indices[ni]

            entries.append({
                "id": old_comp[mi][1].id,
                "flaws": [ images[im_i] ]
            })
        else:
            # possibly detect outliers
            lof = LocalOutlierFactor()
            sims = list(map(lambda m: [ m[0] ], matches))
            labels = lof.fit_predict(sims)

            neg = labels < 0
            pos = labels > 0
            if neg.any():
                out_label = sims[pos].mean() - sims[neg].mean()
            else:
                out_label = 1

            flaws = []
            for (_, ni), label in zip(matches, labels):
                if label * out_label > 0:
                    flaws.append(images[indices[ni]])
                else:
                    outliers.append(ni)
            entries.append({
                "id": old_comp[mi][1].id,
                "flaws": flaws
            })

    # Step 3: Try to cluster outliers together

    for ni in outliers:
        # lulz
        entries.append({
            "id": None,
            "flaws": [ images[indices[ni]] ]
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
