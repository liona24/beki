"""
Script to dump the existing mongodb-using version of bekiga
into an intermediate format (JSON + .png)
"""

from flask import Flask
from flask_pymongo import PyMongo, ObjectId
from gridfs import GridFSBucket, NoFile

import os
import json

CONFIG = {
    "MONGO_PORT": 27017,
    "MONGO_HOST": 'localhost',
    "MONGO_DBNAME": 'bekiga',
}

DST_PATH = "dump"
DST_PATH_IMAGES = "images/"


class FileDownloader:
    fs = None
    fname = None
    revision = None

    def __init__(self, fs, fname, revision=-1):
        self.fs = fs
        self.fname = fname
        self.revision = revision

    def download(self, dst_folder):
        dst = os.path.join(dst_folder, self.fname)
        try:
            with open(dst, 'wb') as dst_file:
                self.fs.download_to_stream_by_name(self.fname,
                                                   dst_file,
                                                   revision=self.revision)
        except NoFile:
            return None

        return self.fname


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, FileDownloader):
            fname = o.download(os.path.join(DST_PATH, DST_PATH_IMAGES))
            if fname is None:
                return ''
            else:
                return os.path.join(DST_PATH_IMAGES, fname)
        else:
            return json.JSONEncoder.default(self, o)


app = Flask(__name__)
for key in CONFIG:
    app.config[key] = CONFIG[key]
mongo = PyMongo(app)


ERRORS = []


def mongo_one(collection, str_id):
    if not str_id:
        ERRORS.append((collection, f"<EMPTY>"))
        return {}
    
    rv = mongo.db[collection].find_one({ '_id': ObjectId(str_id) })
    if rv is None:
        ERRORS.append((collection, str_id))
        return {}
    else:
        return rv


def _resolve_foreign(obj, key, foreign_collection):
    """
    Resolve the value at `key` as foreign key on the given `foreign_collection`
    """
    f_id = obj.get(key, None)
    if f_id is None or not f_id:
        ERRORS.append((foreign_collection, f"<EMPTY> for object with id {str(obj.get('_id', 'NULL'))}"))
        obj[key] = {}
    else:
        obj[key] = mongo_one(foreign_collection, f_id)


def find_full_protocol(str_id):
    """
    Get the protocol with id `str_id`. Resolves all foreign keys. Pictures will
    be available as FileDownloader s.
    Returns a dictionary representing the protocol.
    """
    protocol = {
        'title': '',
        'inspectionOverview': {},
        'inspectionDate': '',
        'attendees': '',
        'facility': '',
        'inspector': '',
        'issuer': '',
        'entries': ""
    }

    protocol.update(mongo_one('protocols', str_id))

    foreigns = [
        ('inspector', 'persons'),
        ('issuer', 'organizations'),
        ('facility', 'facilities'),
        ('inspectionOverview', 'inspectionOverview'),
    ]
    [ _resolve_foreign(protocol, *i) for i in foreigns ]

    _resolve_foreign(protocol['inspector'], 'organization', 'organizations')

    text = protocol['inspectionOverview'].get('text', '')
    protocol['inspectionOverview'] = text.replace('\r\n', '\n').split('\n')

    fs = GridFSBucket(mongo.db, 'files')

    if protocol['facility'].get('picture', False):
        fac = protocol['facility']
        fname = 'facility_' + str(fac['_id']) + '.' + fac['picture']
        protocol['facility']['picture'] = FileDownloader(fs, fname)

    entries = []
    for entry_id in filter(None, protocol['entries'].split(',')):
        entry = {
            'category': '',
            'categoryVersion': '',
            'title': '',
            'manufacturer': '',
            'yearBuilt': '',
            'inspectionSigns': '',
            'manufactureInfoAvailable': '',
            'easyAccess': '',
            'flaws': [],
            'index': '',
        }
        entry.update(mongo_one('entries', entry_id))

        _resolve_foreign(entry, 'category', 'categories')
        standards = []
        inspection_standards = entry['category'].get('inspectionStandards', None)
        if inspection_standards is not None:
            for std_id in inspection_standards.split(','):
                standards.append(mongo_one('inspectionStandards', std_id))

        entry['category']['inspectionStandards'] = standards

        flaws = []
        for flaw_id in entry['flaws'].split(','):
            flaw = {
                'flaw': '',
                'priority': '',
                'notes': '',
                'picture': '',
            }
            flaw.update(mongo_one('flaws', flaw_id))

            if flaw['picture']:
                fname = 'flaw_' + str(flaw['_id']) + '.' + flaw['picture']
                flaw['picture'] = FileDownloader(fs, fname)

            flaws.append(flaw)

        entry['flaws'] = flaws
        entries.append(entry)

    protocol['entries'] = entries

    return protocol


def fetch_all():
    ids = mongo.db.protocols.distinct("_id")

    dumps = []
    for _id in map(str, ids):
        print("Fetching ", _id)
        protocol = find_full_protocol(_id)
        yield protocol


class StreamedList(list):
    def __init__(self, stream):
        self._stream = stream

    def __iter__(self):
        return self._stream

    def __len__(self):
        return 1
    

if __name__ == '__main__':
    if os.path.exists(DST_PATH):
        print(f"WARN: {DST_PATH} exists. Exiting.")
        exit(0)

    os.makedirs(os.path.join(DST_PATH, DST_PATH_IMAGES))
    with app.app_context(), open(os.path.join(DST_PATH, "dump.json"), "w") as f:
        stream = StreamedList(fetch_all())
        json.dump(stream, f, cls=Encoder)

    if len(ERRORS) > 0:
        print("The following references could not be resolved:")
        for coll, id_ in ERRORS:
            print(f"{id_} -> {coll}")
