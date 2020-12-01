from flask import request, abort, jsonify, current_app
import sqlalchemy
from werkzeug.utils import secure_filename

import os
import database
import datetime

db = database.db


class Err(object):
    def __init__(self, msg, target, idx=None):
        self.msg = msg
        self.target = target
        self.idx = idx

    def __dict__(self):
        rv = {
            "msg": self.msg,
            "target": self.target
        }
        if self.idx is not None:
            rv["index"] = self.idx
        return rv


class ErrorAggregator(object):
    def __init__(self):
        self.errors = []
        self.has_errors = []

    def __call__(self, body):
        self.has_errors.append(False)

        def get_param(name, err_or_default, not_empty=True, converter=None):
            if isinstance(err_or_default, Err):
                v = body.get(name, None)

                if converter is not None:
                    v = converter(v)

                if not_empty and not v:
                    v = None
                    self.has_errors[-1] = True
                    self.errors.append(err_or_default.__dict__())
            else:
                v = body.get(name, err_or_default)

                if converter is not None:
                    v = converter(v)

            return v

        return get_param

    def add_error(self, err):
        if len(self.has_errors) > 0:
            self.has_errors[-1] = True
        self.errors.append(err.__dict__())

    def recent_ok(self):
        return not self.has_errors.pop()

    def ok(self):
        return len(self.errors) == 0


def _remove_null_values(dict):
    keys = list(dict.keys())
    for k in keys:
        # this also filters 0 but there is no case in which 0 is acceptable either
        if not dict[k]:
            dict.pop(k)
    return dict


def _checked_picture(pic):
    pic = secure_filename(pic)
    pic = os.path.basename(pic)

    if not pic.endswith(".png"):
        return None

    should_path = os.path.join(current_app.config["IMG_UPLOAD_PATH"], pic)

    if os.path.exists(should_path):
        return pic
    else:
        return None


def _requires_action(body):
    status = body.get("$status", None)
    if status is None:
        abort(400)

    if status == database.SyncStatus.Empty:
        return False, None
    elif (status & database.SyncStatus.Modified) and (status & database.SyncStatus.New):
        return True, None
    elif (status & database.SyncStatus.Stored):
        id = body.get("id", None)
        if id is None:
            abort(400)

        if (status & database.SyncStatus.Modified):
            return True, int(id)
        else:
            return False, int(id)
    else:
        abort(400)


def _fetcher(type):
    def fetch_if_needed(id_or_orm):
        if isinstance(id_or_orm, type):
            return id_or_orm
        elif id_or_orm is not None:
            assert isinstance(id_or_orm, int)

            return db.session.query(type)\
                .filter(type.id == id_or_orm)\
                .first_or_404()
        else:
            return None

    return fetch_if_needed


def _update(type, id, args):
    obj = _fetcher(type)(id)
    for key in args:
        val = getattr(obj, key)
        val = args[key]

    return obj


def _category(body, err_agg):
    action_required, id = _requires_action(body)
    if not action_required:
        return id

    getter = err_agg(body)
    name = getter("name", Err("Feld 'Name' wird benötigt!", "Kategorie"))
    inspection_standards = getter("inspection_standards", [])

    if not isinstance(inspection_standards, list):
        abort(400)

    inspection_standards = list(map(
        _fetcher(database.InspectionStandard),
        filter(
            None,
            map(
                lambda x: _inspection_standard(x, err_agg),
                inspection_standards
            )
        )
    ))

    if err_agg.recent_ok():
        args = _remove_null_values(dict(
            name=name,
            inspection_standards=inspection_standards
        ))
        if id is not None:
            category = _update(database.Category, id, args)
        else:
            category = database.Category(**args)
            db.session.add(category)
        return category
    else:
        return None


def _entry(body, err_agg, idx=None):
    action_required, id = _requires_action(body)
    if not action_required:
        return id

    getter = err_agg(body)
    title = getter("title", Err("Feld 'Titel' wird benötigt!", "Eintrag", idx=idx))
    manufacturer = getter("manufacturer", None)
    year_built = getter("year_built", None)
    inspection_signs = getter("inspection_signs", None)
    manufacture_info_available = getter("manufacture_info_available", "Keine Angabe")
    easy_access = getter("easy_access", "Keine Angabe")

    index = getter("index", Err("Feld 'Index' wird benötigt!", "Eintrag", idx=idx))
    category = getter("category", Err("Feld 'Kategorie' wird benötigt!", "Eintrag", idx=idx))
    category_version = getter("category_version", Err("Feld 'Version' wird benötigt!", "Eintrag", idx=idx))

    flaws = getter("flaws", [])

    if not isinstance(flaws, list):
        abort(400)

    if len(flaws) > 3:
        err_agg.add_error(Err("Maximal 3 Mängel pro Eintrag!", "Eintrag", idx=idx))
    else:
        flaws = list(map(
            _fetcher(database.Flaw),
            filter(
                None,
                map(
                    lambda x: _flaw(x[1], err_agg, idx=x[0]),
                    enumerate(flaws)
                )
            )
        ))

    if category is not None:
        category = _fetcher(database.Category)(
            _category(category, err_agg)
        )

    if err_agg.recent_ok():
        args = _remove_null_values(dict(
            title=title,
            manufacturer=manufacturer,
            year_built=year_built,
            inspection_signs=inspection_signs,
            manufacture_info_available=manufacture_info_available,
            easy_acces=easy_access,
            index=index,
            category=category,
            category_version=category_version,
            flaws=flaws
        ))
        if id is not None:
            obj = _update(database.Entry, id, args)
        else:
            obj = database.Entry(**args)
            db.session.add(obj)
        return obj
    else:
        return None


def _facility(body, err_agg):
    action_required, id = _requires_action(body)
    if not action_required:
        return id

    getter = err_agg(body)
    name = getter("name", Err("Feld 'Name' wird benötigt!", "Objekt"))
    street = getter("street", Err("Feld 'Straße/Nr.' wird benötigt!", "Objekt"))
    zip_code = getter("zip_code", Err("Feld 'Postleitzahl' wird benötigt!", "Objekt"))
    city = getter("city", Err("Feld 'Stadt' wird benötigt!", "Objekt"))
    picture = getter("picture", None, not_empty=False)

    if _checked_picture(picture) != picture:
        err_agg.add_error(Err("Das angegebene Bild konnte nicht gefunden werden!", "Objekt"))
        picture = None

    if err_agg.recent_ok():
        args = _remove_null_values(dict(
            name=name,
            street=street,
            zip_code=zip_code,
            city=city,
            picture=picture,
        ))
        if id is not None:
            obj = _update(database.Facility, id, args)
        else:
            obj = database.Facility(**args)
            db.session.add(obj)
        return obj
    else:
        return None


def _flaw(body, err_agg, idx=None):
    action_required, id = _requires_action(body)
    if not action_required:
        return id

    getter = err_agg(body)
    title = getter("title", Err("Feld 'Titel' wird benötigt!", "Mangel", idx=idx))
    notes = getter("notes", "")
    priority = getter("priority", "")
    picture = getter("picture", None, not_empty=False)

    if _checked_picture(picture) != picture:
        err_agg.add_error(Err("Das angegebene Bild konnte nicht gefunden werden!", "Mangel", idx=idx))
        picture = None

    if err_agg.recent_ok():
        args = _remove_null_values(dict(
            title=title,
            notes=notes,
            priority=priority,
            picture=picture,
        ))
        if id is not None:
            flaw = _update(database.Flaw, id, args)
        else:
            flaw = database.Flaw(**args)
            db.session.add(flaw)
        return flaw
    else:
        return None


def _inspection_standard(body, err_agg):
    action_required, id = _requires_action(body)
    if not action_required:
        return id

    getter = err_agg(body)
    din = getter("din", Err("Feld 'DIN' wird benötigt!", "Prüfkriterium"))
    description = getter("description", "")
    has_version = getter("has_version", Err("Feld 'Versioniert' wird benötigt!", "Prüfkriterium"))

    if err_agg.recent_ok():
        args = _remove_null_values(dict(
            din=din,
            description=description,
            has_version=has_version,
        ))
        if id is not None:
            std = _update(database.InspectionStandard, id, args)
        else:
            std = database.InspectionStandard(**args)
            db.session.add(std)
        return std
    else:
        return None


def _organization(body, err_agg):
    action_required, id = _requires_action(body)
    if not action_required:
        return id

    getter = err_agg(body)
    name = getter("name", Err("Feld 'Name' wird benötigt!", "Organisation"))
    street = getter("street", Err("Feld 'Straße/Nr.' wird benötigt!", "Organisation"))
    zip_code = getter("zip_code", Err("Feld 'Postleitzahl' wird benötigt!", "Organisation"))
    city = getter("city", Err("Feld 'Stadt' wird benötigt!", "Organisation"))

    if err_agg.recent_ok():
        args = _remove_null_values(dict(
            name=name,
            street=street,
            zip_code=zip_code,
            city=city
        ))
        if id is not None:
            obj = _update(database.Organization, id, args)
        else:
            obj = database.Organization(**args)
            db.session.add(obj)
        return obj
    else:
        return None


def _person(body, err_agg):
    action_required, id = _requires_action(body)
    if not action_required:
        return id

    getter = err_agg(body)
    name = getter("name", Err("Feld 'Name' wird benötigt!", "Person"))
    first_name = getter("first_name", None, not_empty=False)
    email = getter("email", None, not_empty=False)
    organization = getter(
        "organization",
        Err("Feld 'Organisation' wird benötigt!", "Person"),
        converter=lambda v: _fetcher(database.Organization)(_organization(v, err_agg))
    )

    if err_agg.recent_ok():
        args = _remove_null_values(dict(
            name=name,
            first_name=first_name,
            email=email,
            organization=organization
        ))
        if id is not None:
            obj = _update(database.Person, id, args)
        else:
            obj = database.Person(**args)
            db.session.add(obj)
        return obj
    else:
        return None


def _protocol(body, err_agg):
    action_required, id = _requires_action(body)
    if not action_required:
        return id

    getter = err_agg(body)
    title = getter("title", Err("Feld 'Titel' wird benötigt!", "Protokoll"))
    overview = getter("overview", Err("Feld 'Prüfgrundlagen' wird benötigt!", "Protokoll"))
    inspection_date = getter("inspection_date", Err("Feld 'Prüfdatum' wird benötigt!", "Protokoll"))
    attendees = getter("attendees", None)

    inspector = getter(
        "inspector",
        Err("Feld 'Prüfer' wird benötigt!", "Protokoll"),
        converter=lambda v: _fetcher(database.Person)(_person(v, err_agg))
    )
    facility = getter(
        "facility",
        Err("Feld 'Objekt' wird benötigt!", "Protokoll"),
        converter=lambda v: _fetcher(database.Facility)(_facility(v, err_agg))
    )
    issuer = getter(
        "issuer",
        Err("Feld 'Auftraggeber' wird benötigt!", "Protokoll"),
        converter=lambda v: _fetcher(database.Organization)(_organization(v, err_agg))
    )

    entries = getter("entries", [])

    if not isinstance(entries, list):
        abort(400)

    entries = list(map(
        _fetcher(database.Entry),
        filter(
            None,
            map(
                lambda x: _entry(x[1], err_agg, idx=x[0]),
                enumerate(entries)
            )
        )
    ))

    if inspection_date is not None:
        inspection_date = datetime.date.fromisoformat(inspection_date)

    if err_agg.recent_ok():
        args = _remove_null_values(dict(
            title=title,
            overview=overview,
            inspection_date=inspection_date,
            attendees=attendees,
            inspector=inspector,
            facility=facility,
            issuer=issuer,
            entries=entries
        ))
        if id is not None:
            # TODO: make sure that this is used correctly w.r.t legacy protocols
            obj = _update(database.Protocol, id, args)
        else:
            # TODO: update legacy protocols
            obj = database.Protocol(**args)
            db.session.add(obj)
        return obj
    else:
        return None


HANDLERS = {
    "category": _category,
    "entry": _entry,
    "facility": _facility,
    "flaw": _flaw,
    "inspection_standard": _inspection_standard,
    "organization": _organization,
    "person": _person,
    "protocol": _protocol
}

def api_post(collection):
    handler = HANDLERS.get(collection, None)
    if handler is None:
        abort(400)

    err_agg = ErrorAggregator()
    id = None

    rv = handler(request.json, err_agg)

    if err_agg.ok():
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            err_agg.add_error(Err("Integrität verletzt. Ausführung abgebrochen.", "Fehler"))
        else:
            id = rv.id

    return jsonify(id=id, errors=err_agg.errors)
