import os
import sys
from itertools import chain
import datetime

path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(path)

from flask import Flask
import database

app = Flask(__name__)

db_path = "/tmp/beki.db"
if os.path.exists(db_path):
    print("WARNING: Database exists. Overwriting.")
    os.remove(db_path)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

database.init_db(app)
db = database.db
with app.app_context():
    db.create_all(app=app)

    flaws = [
        database.Flaw(
            title="Mangel 1",
            notes="Hinweise 1\nBla Foo\nZeile 3",
            priority="Prio: sofort",
        ),
        database.Flaw(
            title="MaNGel 2",
            notes="HINweise 2\nFoo Bar\nZeile 3\nZeile 4",
            priority="Prio: später",
        ),
        database.Flaw(
            title="MaNGEL 3",
            notes="HinWEIse 3\nFoo bAr\nZeile 3",
            priority="Prio: egal",
        ),
        database.Flaw(
            title="mANgel 4",
            notes="HinWEIse 2\nFOO bAr\nZEILE 3\nZeile 4",
            priority="Prio: niew",
        ),
    ]

    orgs = [
        database.Organization(
            name="Organisation 1",
            street="Irgendwo 123",
            zip_code="02334",
            city="Musterstadt"
        ),
        database.Organization(
            name="Firma 2",
            street="Nirgendwo 84",
            zip_code="91382",
            city="Dorf"
        )
    ]

    facilities = [
        database.Facility(
            name="Kiga 1",
            street="Spielstraße 23",
            zip_code="12345",
            city="Kinderstadt",
        ),
        database.Facility(
            name="Gika 129",
            street="Hauptstraße 4393",
            zip_code="89735",
            city="Rentnerstadt",
        ),
        database.Facility(
            name="Migka 129",
            street="Hinterland 2",
            zip_code="02931",
            city="Wald",
        ),
    ]

    insp_stads = [
        database.InspectionStandard(
            din="DIN 1",
            description="B1schre1bung DIN 1",
            has_version="Ja"
        ),
        database.InspectionStandard(
            din="DIN 2",
            description="B2schr2ibung DIN 2",
            has_version="Nein"
        ),
        database.InspectionStandard(
            din="DIN 3",
            description="B3schr3ibung DIN 3",
            has_version="Nein"
        ),
    ]

    for obj in chain(flaws, orgs, facilities, insp_stads):
        db.session.add(obj)
    db.session.commit()

    persons = [
        database.Person(
            name="Karl",
            first_name="Marx",
            email="karl@red.com",
            organization_id=orgs[0].id
        ),
        database.Person(
            name="Mann",
            first_name="Max",
            email="max@thereal.de",
            organization=orgs[1]
        ),
    ]

    categories = [
        database.Category(
            name="Kategorie 1",
            inspection_standards=[insp_stads[0]]
        ),
        database.Category(
            name="KateGORie 2",
            inspection_standards=[insp_stads[1], insp_stads[2]]
        )
    ]

    for obj in chain(categories, persons):
        db.session.add(obj)
    db.session.commit()

    entries = [
        database.Entry(
            title="Rutsche",
            manufacturer="Rutschenbauer '94 GmbH",
            year_built=1999,
            inspection_signs="CE, DIN",

            manufacture_info_available="Ja",
            easy_access="Ja",

            index=1,
            category_id=categories[0].id,
            category_version=2020,

            flaws=[flaws[0], flaws[1], flaws[2]],
        ),
        database.Entry(
            title="Schaukel",
            manufacturer="Swing GmbH",
            year_built=2002,
            inspection_signs="DIN",

            manufacture_info_available="Keine Angabe",
            easy_access="Nein",

            index=2,
            category_id=categories[1].id,
            category_version=2018,

            flaws=[flaws[3]],
        )
    ]

    for obj in entries:
        db.session.add(obj)
    db.session.commit()

    protocols = [
        database.Protocol(
            title="Protokoll 1",
            overview="Übersicht Zeile 1\nZeil 2\nZeile alsdkjasdjaslkdjasdla\nZeile 4",
            facility_id=facilities[0].id,
            inspection_date=datetime.date(2020, 3, 23),
            attendees="Peter Klause, Klause Schmidt",
            inspector_id=persons[0].id,
            issuer_id=orgs[0].id,
            entries=entries,
        ),
        database.Protocol(
            title="ProTOKoll 2",
            overview="Übersicht Zeile 1\nZeil 2\nZeile alsdkjasdjaslkdjasdla\nZeile 4",
            facility_id=facilities[1].id,
            inspection_date=datetime.date(2020, 10, 16),
            attendees="P. Jama",
            inspector_id=persons[1].id,
            issuer_id=orgs[0].id,
            entries=entries,
        ),
        database.Protocol(
            title="Baarl 3",
            overview="ÜbeRSICHT Zeile 1\nZeil 2\nZeile alsdkjasdjaslkdjasdla\nZeile 4",
            facility_id=facilities[2].id,
            inspection_date=datetime.date(2020, 4, 4),
            attendees="P. Swat",
            inspector_id=persons[0].id,
            issuer_id=orgs[1].id,
            entries=[],
        )
    ]

    for obj in protocols:
        db.session.add(obj)
    db.session.commit()
