from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.attributes import CollectionAttributeImpl

from enum import IntFlag, IntEnum


db = SQLAlchemy()


def init_db(app):
    db.init_app(app)


class CommonType(IntEnum):
    Unknown = -1

    Protocol = 1
    Facility = 2
    Organization = 3
    Person = 4
    InspectionStandard = 5
    Category = 6
    Entry = 7
    Flaw = 8


class SyncStatus(IntFlag):
    Empty = 0
    Modified = 1
    New = 2
    AwaitsConfirmation = 4

    Lazy = 32
    Stored = 64


class Serializer(object):

    @property
    def common_type(self):
        return CommonType.Unknown

    def common_repr(self):
        return "<UNKNOWN>"

    def serialize(self, full=False):
        # these are some ugly hacks in order to prevent lazy fetching
        # for relationships
        # Therefor we apply the following heuristic:
        # If a field ends with 'id' we assume that a corresponding
        # relationship exists and we actively skip it if we
        # do a shallow serialization (full = false).
        # If we do a deep serialization we do exactly the opposite.
        # The only special case is 'id' itself, corresponding to the
        # primary key of 'self'

        attrs = set(inspect(self).attrs.keys())
        ids = list(filter(lambda x: x.endswith("_id"), attrs))

        rv = {}
        if full:
            for id in ids:
                attrs.remove(id)
        else:
            for id in ids:
                rv[id] = getattr(self, id)
                attrs.remove(id[:-3])

        for a in attrs:
            if isinstance(getattr(self.__class__, a).impl, CollectionAttributeImpl):
                # prevent lazy loading for many-to-* associations
                if not full:
                    continue
                else:
                    rv[a] = [ el.serialize(full) for el in getattr(self, a) ]
            else:
                val = getattr(self, a)
                if isinstance(val, Serializer):
                    val = val.serialize(full)
                rv[a] = val

        rv["$status"] = SyncStatus.Stored
        if not full:
            rv["$status"] |= SyncStatus.Lazy

        rv["$type"] = self.common_type
        rv["$repr"] = self.common_repr()

        return rv


class Settings(db.Model, Serializer):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)

    image_width = db.Column(db.Integer, nullable=False)
    image_height = db.Column(db.Integer, nullable=False)


class Facility(db.Model, Serializer):
    __tablename__ = "facility"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    street = db.Column(db.String)
    zip_code = db.Column(db.String)
    city = db.Column(db.String)
    picture = db.Column(db.String)

    autocompleteable = ()
    discoverable = "name", "street", "city", "zip_code"

    @property
    def common_type(self):
        return CommonType.Facility

    def common_repr(self):
        return f"{self.name}, {self.city}"


class Protocol(db.Model, Serializer):
    __tablename__ = "protocol"

    id = db.Column(db.Integer, primary_key=True)

    facility_id = db.Column(db.Integer, db.ForeignKey("facility.id"), nullable=False, unique=True)
    facility = db.relationship("Facility", foreign_keys=facility_id)

    title = db.Column(db.String, nullable=False)
    overview = db.Column(db.String, nullable=False)
    inspection_date = db.Column(db.Date, nullable=False)
    attendees = db.Column(db.String)

    inspector_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)
    inspector = db.relationship("Person", foreign_keys=inspector_id)

    entries = db.relationship("Entry", secondary="protocol_entry")

    autocompleteable = "title", "overview"
    discoverable = "title", "inspection_date", "attendees", Facility

    @property
    def common_type(self):
        return CommonType.Protocol

    def common_repr(self):
        return self.title


class Person(db.Model, Serializer):
    __tablename__ = "person"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)

    email = db.Column(db.String)

    organization_id = db.Column(db.Integer, db.ForeignKey("organization.id"))
    organization = db.relationship("Organization", foreign_keys=organization_id)

    discoverable = "name", "first_name", "email"
    autocompleteable = ()

    @property
    def common_type(self):
        return CommonType.Person

    def common_repr(self):
        return f"{self.name}, {self.first_name}"


class Category(db.Model, Serializer):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, unique=True, nullable=False)

    inspection_standards = db.relationship("InspectionStandard", secondary="category_inspection_standard")

    autocompleteable = ()
    discoverable = "name",

    @property
    def common_type(self):
        return CommonType.Category

    def common_repr(self):
        return self.name


class InspectionStandard(db.Model, Serializer):
    __tablename__ = "inspection_standard"

    id = db.Column(db.Integer, primary_key=True)

    din = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    has_version = db.Column(db.String, nullable=False)

    autocompleteable = ()
    discoverable = "din", "description"

    @property
    def common_type(self):
        return CommonType.InspectionStandard

    def common_repr(self):
        v = ''
        if self.has_version.startswith('Ja'):
            v = '(V)'
        return f"DIN {v} {self.din} {self.description}"


class Organization(db.Model, Serializer):
    __tablename__ = "organization"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    street = db.Column(db.String, nullable=False)
    zip_code = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)

    autocompleteable = ()
    discoverable = "name", "street", "zip_code", "city"

    @property
    def common_type(self):
        return CommonType.Organization

    def common_repr(self):
        return f"{self.name}, {self.city}"


class Flaw(db.Model, Serializer):
    __tablename__ = "flaw"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False)
    notes = db.Column(db.String)
    priority = db.Column(db.String)
    picture = db.Column(db.String)

    autocompleteable = "title", "notes", "priority"
    discoverable = ()

    @property
    def common_type(self):
        return CommonType.Flaw

    def common_repr(self):
        return self.title


class Entry(db.Model, Serializer):
    __tablename__ = "entry"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False)
    manufacturer = db.Column(db.String)
    year_built = db.Column(db.Integer)
    inspection_signs = db.Column(db.String)

    manufacture_info_available = db.Column(db.String)
    easy_access = db.Column(db.String)

    index = db.Column(db.Integer, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", foreign_keys=category_id)
    category_version = db.Column(db.Integer, nullable=False)

    flaws = db.relationship("Flaw", secondary="entry_flaw")

    autocompleteable = "title", "manufacturer", "inspection_signs"
    discoverable = ()

    @property
    def common_type(self):
        return CommonType.Entry

    def common_repr(self):
        return self.title


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


TABLES = {
    "category": Category,
    "entry": Entry,
    "facility": Facility,
    "flaw": Flaw,
    "inspection_standard": InspectionStandard,
    "organization": Organization,
    "person": Person,
    "protocol": Protocol
}
