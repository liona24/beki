from flask import Flask, request, jsonify, abort
import database

import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///beki.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

database.init_db(app)
db = database.db

# vuesax

if not os.path.exists("beki.db"):
    with app.app_context():
        db.create_all(app=app)


def int_or_404(string):
    try:
        rv = int(string)
    except ValueError:
        abort(404)

    return rv


@app.route("/api/protocol", methods=["GET", "POST"])
def api_protocol():
    if request.method == "GET":
        id = request.args.get("id", None)
        if id is None:
            abort(400)

        id = int_or_404(id)

        protocol = db.session.query(database.Protocol)
            .filter(database.Protocol.id == id)
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
            id = int_or_404(request.form.pop("id"))

            protocol = db.session.query(database.Protocol)
                .filter(database.Protocol.id == id)
                .first()

            if protocol is not None:
                entries = list(protocol.entries)

                db.session.query(database.ProtocolEntry)
                    .filter(database.ProtocolEntry.protocol_id == id)
                    .delete()



        db.session.commit()

        return 201
    else:
        raise NotImplementedError(f"Method {request.method} for /api/protocol not implemented!")

@app.route("/api/protocol", methods=["GET", "POST"])
def api_protocol():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass
