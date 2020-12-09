"""
This script uploads a dump generated with 'dump_mongo.py'
to the new server
"""

import os
import sys
import json
import datetime
from collections import defaultdict

import requests

# With this script only the last protocol can be kept right now
# The problem is the auto-cleanup feature of the server
# In order to support more, just disable it temporarly
N_LATEST_TO_KEEP = 1


def upload_img(base_url, filename):
    url = base_url + "/api/_upload"
    name = "foo.png"
    files = { name: open(filename, "rb") }
    resp = requests.post(url, files=files)
    resp.raise_for_status()
    resp = resp.json()
    print(f"upload {filename} -> {resp[name]}")
    return resp[name]


def upload_json(base_url, type, obj):
    url = base_url + "/api/" + type
    resp = requests.post(url, json=obj)
    resp.raise_for_status()
    resp = resp.json()
    id_ = resp["id"]

    if len(resp["errors"]) > 0:
        print(resp["errors"])
        print(" for ", json.dumps(obj))
        exit(3)

    print(f"{type} {obj['_id']} -> {id_}")
    return id_


def defer(value, storage):
    _id = value["_id"]
    if _id not in storage:
        storage[_id] = value

    return (_id, storage)


def resolve(deferred):
    _id, item = deferred
    # this is a little trick to tell the server to do everything
    return { "$status": 64, "id": item[_id] }


def inv_camel_case(camel_case):
    camel_case = iter(camel_case)
    result = [ next(camel_case) ]
    for c in camel_case:
        if c.isupper():
            result.append('_')
        result.append(c.lower())

    return ''.join(result)


def prepare(obj):
    assert isinstance(obj, dict)

    keys = list(obj.keys())

    for k in keys:
        value = obj.pop(k)

        new_k = inv_camel_case(k)

        assert not isinstance(value, dict), f"Missed a reference? {value}"

        if isinstance(value, list):
            value = list(map(resolve, value))
        elif isinstance(value, tuple):
            value = resolve(value)

        obj[new_k] = value

    obj["id"] = None
    obj["$status"] = 3  # New | Modified

    return obj


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <PATH TO DUMP DIRECTORY> <BEKI URL>")
        exit(1)


    dump_dir = sys.argv[1]
    dump_json = os.path.join(dump_dir, "dump.json")

    url = sys.argv[2].rstrip("/")

    print(f"Processing {dump_dir} ..")

    with open(dump_json, "r") as f:
        dump = json.load(f)

    print(f"Keeping the last {N_LATEST_TO_KEEP} versions for each facility ..")

    protocols_to_keep = defaultdict(list)

    while len(dump) > 0:
        protocol = dump.pop()

        facility = protocol.get('facility', None)
        if facility is None:
            continue

        name = facility.get("name", None)
        if name is None:
            continue

        name = name.strip()
        if not name:
            continue

        if not protocol.get("inspectionDate", None):
            continue

        protocols_to_keep[name].append(protocol)
        if len(protocols_to_keep[name]) > N_LATEST_TO_KEEP:
            protocols_to_keep[name].sort(
                key=lambda p: p["inspectionDate"],
                reverse=True
            )
            protocols_to_keep[name].pop()

    print(f"Transforming into new schema ..")

    protocols = []

    for name in protocols_to_keep:
        dates = set()
        for protocol in reversed(protocols_to_keep[name]):
            if protocol["inspectionDate"] not in dates:
                protocols.append(protocol)
                dates.add(protocol["inspectionDate"])

    # in order to avoid duplication we will replace all objects
    # with lazy refs

    facility = {}
    person = {}
    organization = {}

    flaw = {}
    entry = {}

    inspection_standard = {}
    category = {}

    for p in protocols:
        p["facility"] = defer(p["facility"], facility)

        ip = p["inspector"]
        ip["organization"] = defer(ip["organization"], organization)
        p["inspector"] = defer(ip, person)

        p["issuer"] = defer(p["issuer"], organization)

        io = p.pop("inspectionOverview")
        p["overview"] = "\r\n".join(io)

        entries = []
        for e in p["entries"]:
            if "_id" not in e:
                print("WARN: missing id:", json.dumps(e))
                continue

            if not e["title"]:
                print("WARN: empty entry:", json.dumps(e))
                continue

            cat = e["category"]
            iss = []
            for i in cat["inspectionStandards"]:
                iss.append(defer(i, inspection_standard))
            cat["inspectionStandards"] = iss
            e["category"] = defer(cat, category)

            flaws = []
            for f in e["flaws"]:
                if "_id" not in f:
                    print("WARN: missing id:", json.dumps(f))
                    continue

                flaws.append(defer(f, flaw))

                if len(flaws) == 5:
                    # whatever, just drop em
                    break

            e["flaws"] = flaws

            entries.append(defer(e, entry))
        p["entries"] = entries

    # we can now add the simple objects
    print("Trying to find recovery point ..")
    recov_path = os.path.join(dump_dir, "upload.json")
    if os.path.exists(recov_path):
        print(f"Found. Using '{recov_path}' to fast forward upload.")
        with open(recov_path, "r") as f:
            upload = json.load(f)

        facility.update(upload.get("facility", {}))
        person.update(upload.get("person", {}))
        organization.update(upload.get("organization", {}))
        category.update(upload.get("category", {}))
        inspection_standard.update(upload.get("inspection_standard", {}))
        entry.update(upload.get("entry", {}))
        flaw.update(upload.get("flaw", {}))
    else:
        upload = {}


    print("Uploading facilities ..")
    n_skipped = 0
    for k in facility:
        if not isinstance(facility[k], dict):
            n_skipped += 1
            continue

        obj = prepare(facility[k])
        pic = obj.get("picture", None)
        if pic:
            obj["picture"] = upload_img(url, os.path.join(dump_dir, pic))

        facility[k] = upload_json(url, "facility", obj)

    upload["facility"] = facility
    with open(recov_path, "w") as f:
        json.dump(upload, f)

    print(f"Done. ({n_skipped} skipped.)")

    print()
    print("Uploading organizations ..")
    n_skipped = 0
    for k in organization:
        if not isinstance(organization[k], dict):
            n_skipped += 1
            continue

        obj = prepare(organization[k])

        organization[k] = upload_json(url, "organization", obj)

    upload["organization"] = organization
    with open(recov_path, "w") as f:
        json.dump(upload, f)

    print(f"Done. ({n_skipped} skipped.)")

    print()
    print("Uploading persons ..")
    n_skipped = 0
    for k in person:
        if not isinstance(person[k], dict):
            n_skipped += 1
            continue

        obj = prepare(person[k])

        person[k] = upload_json(url, "person", obj)

    upload["person"] = person
    with open(recov_path, "w") as f:
        json.dump(upload, f)

    print(f"Done. ({n_skipped} skipped.)")

    print()
    print("Uploading inspection standards ..")
    n_skipped = 0
    for k in inspection_standard:
        if not isinstance(inspection_standard[k], dict):
            n_skipped += 1
            continue
        obj = prepare(inspection_standard[k])

        inspection_standard[k] = upload_json(url, "inspection_standard", obj)

    upload["inspection_standard"] = inspection_standard
    with open(recov_path, "w") as f:
        json.dump(upload, f)

    print(f"Done. ({n_skipped} skipped.)")

    print()
    print("Uploading categories ..")
    n_skipped = 0
    for k in category:
        if not isinstance(category[k], dict):
            n_skipped += 1
            continue
        obj = prepare(category[k])

        category[k] = upload_json(url, "category", obj)

    upload["category"] = category
    with open(recov_path, "w") as f:
        json.dump(upload, f)

    print(f"Done. ({n_skipped} skipped.)")

    print()
    print("Uploading flaws ..")
    n_skipped = 0
    for k in flaw:
        if not isinstance(flaw[k], dict):
            n_skipped += 1
            continue

        obj = prepare(flaw[k])

        title = obj.pop("flaw")
        obj["title"] = title

        pic = obj.get("picture", None)
        if pic:
            obj["picture"] = upload_img(url, os.path.join(dump_dir, pic))

        flaw[k] = upload_json(url, "flaw", obj)

    upload["flaw"] = flaw
    with open(recov_path, "w") as f:
        json.dump(upload, f)

    print(f"Done. ({n_skipped} skipped.)")

    print()
    print("Uploading entries ..")
    n_skipped = 0
    for k in entry:
        if not isinstance(entry[k], dict):
            n_skipped += 1
            continue

        obj = prepare(entry[k])

        entry[k] = upload_json(url, "entry", obj)

    upload["entry"] = entry
    with open(recov_path, "w") as f:
        json.dump(upload, f)

    print(f"Done. ({n_skipped} skipped.)")

    print()
    print("Uploading protocols ..")
    for p in protocols:
        obj = prepare(p)

        upload_json(url, "protocol", obj)

    print()
    print("Done.")
