from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect


db = SQLAlchemy()


def init_db(app):
    db.init_app(app)


class Serializer(object):

    def serialize(self):
        return { c: getattr(self, c) for c in inspect(self).attrs.keys() }


class Settings(db.Model, Serializer):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)

    image_width = db.Column(db.Integer, nullable=False)
    image_height = db.Column(db.Integer, nullable=False)


class Protocol(db.Model, Serializer):
    __tablename__ = "protocol"

    # TODO: consider making facility_id unique? All the old protocols are then
    # archived in LegacyProtocol or smth

    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey("facility.id"), nullable=False, unique=True)

    number_of_old_version = db.Column(db.Integer, nullable=False)

    title = db.Column(db.String, nullable=False)
    inspection_date = db.Column(db.Date)
    attendees = db.Column(db.String)

    inspector_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)
    overview_id = db.Column(db.Integer, db.ForeignKey("overview.id"), nullable=False)

    entries = db.relationship("Entry", secondary="protocol_entry")


class Person(db.Model, Serializer):
    __tablename__ = "person"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)

    email = db.Column(db.String)

    organization_id = db.Column(db.Integer, db.ForeignKey("organization.id"))


class Category(db.Model, Serializer):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)

    inspection_standards = db.relationship("InspectionStandard", secondary="category_inspection_standard")


class Facility(db.Model, Serializer):
    __tablename__ = "facility"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    street = db.Column(db.String)
    zip_code = db.Column(db.String)
    city = db.Column(db.String)
    picture = db.Column(db.String)


class Overview(db.Model, Serializer):
    __tablename__ = "overview"

    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.String, nullable=False)


class InspectionStandard(db.Model, Serializer):
    __tablename__ = "inspection_standard"

    id = db.Column(db.Integer, primary_key=True)

    din = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    versioned = db.Column(db.Boolean)


class Organization(db.Model, Serializer):
    __tablename__ = "organization"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    street = db.Column(db.String)
    zip_code = db.Column(db.String)
    city = db.Column(db.String)


class Flaw(db.Model, Serializer):
    __tablename__ = "flaw"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False)
    notes = db.Column(db.String)
    priority = db.Column(db.String)
    picture = db.Column(db.String)


class Entry(db.Model, Serializer):
    __tablename__ = "entry"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False)
    manufacturer = db.Column(db.String)
    year_built = db.Column(db.Integer)
    inspection_signs = db.Column(db.String)

    manufacture_infdbation_available = db.Column(db.Boolean)
    easily_accessible = db.Column(db.Boolean)

    index = db.Column(db.Integer, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category_version = db.Column(db.Integer, nullable=False)

    flaws = db.relationship("Flaw", secondary="EntryFlaw")


class ImageFeature(db.Model):
    __tablename__ = "image_feature"

    feature = db.Column(db.String, primary_key=True)
    image = db.Column(db.String, primary_key=True)


class ProtocolEntry(db.Model):
    __tablename__ = "protocol_entry"

    protocol_id = db.Column(db.Integer, db.ForeignKey("protocol.id"), primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey("entry.id"), primary_key=True)


class CategoryInspectionStandard(db.Model):
    __tablename__ = "category_inspection_standard"

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), primary_key=True)
    inspection_standard_id = db.Column(db.Integer, db.ForeignKey("inspection_standard.id"), primary_key=True)


class EntryFlaw(db.Model):
    __tablename__ = "entry_flaw"

    entry_id = db.Column(db.Integer, db.ForeignKey("entry.id"), primary_key=True)
    flaw_id = db.Column(db.Integer, db.ForeignKey("flaw.id"), primary_key=True)
