from flask import Flask, request, jsonify, abort
from sqlalchemy import or_
import database

import os

app = Flask(__name__)

DB_PATH = "/tmp/beki.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_PATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

database.init_db(app)
db = database.db


def int_or_400(string):
    try:
        rv = int(string)
    except ValueError:
        abort(400)

    return rv


def param_or_400(name):
    rv = request.json.get(name, None)
    if rv is None:
        abort(400)
    return rv


@app.route("/api/protocol", methods=["GET", "POST"])
def api_protocol():
    if request.method == "GET":
        id = request.args.get("id", None)
        if id is None:
            abort(400)

        id = int_or_404(id)

        protocol = db.session.query(database.Protocol)\
            .filter(database.Protocol.id == id)\
            .first()

        if protocol is None:
            return jsonify(None)

        # TODO: We probably want to fetch all the entries (ids)
        # We could also fetch everything here but I assume it is better for
        # lazy loading if we only fetch the ids of everything

        protocol = protocol.serialize()
        return protocol
    elif request.method == "POST":
        if id in request.form:
            id = int_or_400(request.form.pop("id"))

            protocol = db.session.query(database.Protocol)\
                .filter(database.Protocol.id == id)\
                .first()

            if protocol is not None:
                entries = list(protocol.entries)

                db.session.query(database.ProtocolEntry)\
                    .filter(database.ProtocolEntry.protocol_id == id)\
                    .delete()



        db.session.commit()

        return 201
    else:
        raise NotImplementedError(f"Method {request.method} for /api/protocol not implemented!")


def escape_for_like_query(query):
    return query.replace("%", r"\%")


def get_column(table, name):
    return table.__table__.columns[name]


def generic_autocomplete_handler(table, key, query):
    if key not in table.autocompleteable:
        abort(404)

    query = escape_for_like_query(query)

    column = get_column(table, key)
    result = db.session.query(column)\
        .filter(column.like(f"%{query}%"))\
        .distinct()\
        .limit(10)\
        .all()

    return jsonify(list(map(lambda record: record[0], result)))


def generic_discover_handler(table, query):
    if len(table.discoverable) == 0:
        abort(404)

    query = escape_for_like_query(query)
    like_query = f"%{query}%"

    query_builder = db.session.query(table)
    columns = [ (table, name) for name in table.discoverable ]
    conditions = []
    i = 0
    while i < len(columns):
        table, name = columns[i]
        if type(name) == str:
            conditions.append(get_column(table, name).like(like_query))
        else:
            # name is actually another table reference
            table = name
            columns.extend([ (table, name) for name in table.discoverable ])
            query_builder = query_builder.join(table)

        i += 1

    result = query_builder\
        .filter(or_(*conditions))\
        .distinct()\
        .limit(10)\
        .all()

    return jsonify(list(map(lambda record: record.serialize(), result)))


@app.route("/api/_autocomplete", methods=["GET", "POST"])
def autocomplete():
    query = param_or_400("q")
    if len(query) < 2:
        abort(400)

    data_src = param_or_400("src")
    key = param_or_400("key")

    table = database.TABLES.get(data_src, None)
    if table is None:
        abort(404)

    return generic_autocomplete_handler(table, key, query)


@app.route("/api/_discover", methods=["GET", "POST"])
def discover():
    query = param_or_400("q")
    if len(query) < 2:
        abort(400)

    data_src = param_or_400("src")

    table = database.TABLES.get(data_src, None)
    if table is None:
        abort(404)

    return generic_discover_handler(table, query)

@app.route("/api/<collection>/<int:id>", methods=["GET"], defaults={'recursive': False})
@app.route("/api/<collection>/<int:id>/recursive", methods=["GET"], defaults={'recursive': True})
def api_get(collection, id, recursive):
    table = database.TABLES.get(collection, None)
    if table is None:
        abort(404)

    result = db.session.query(table)\
        .filter(getattr(table, "id") == id)\
        .first_or_404()

    return jsonify(result.serialize(full=recursive))

if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)
