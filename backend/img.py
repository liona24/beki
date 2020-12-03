from flask import current_app
import cv2 as cv

import os
import numpy as np
import hashlib


def _read_file(file):
    in_buf = file.read()
    in_buf = np.asarray(bytearray(in_buf), dtype=np.uint8)
    img = cv.imdecode(in_buf, cv.IMREAD_COLOR)

    return img


def _store_unified(img):
    w, h = current_app.config["IMG_CROP_SIZE"]
    assert w != h, "TODO we might want to actually crop the image"
    img = cv.resize(img, (w, h), interpolation=cv.INTER_AREA)

    _, out_buf = cv.imencode(".png", img)
    out_buf = bytes(out_buf)
    h = hashlib.sha1()
    h.update(out_buf)
    file_name = h.hexdigest() + ".png"

    dst_path = os.path.join(current_app.config["IMG_UPLOAD_PATH"], file_name)
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


def upload_img_file(file):
    img = _read_file(file)
    if img is None:
        return None

    return _store_unified(img)
