"""
Flask CRUD Application with SQLite and JSON Schema Validation
=============================================================
Endpoints:
  POST   /person        — Create a new person
  GET    /person         — List all people
  GET    /person/<id>    — Get a single person
  PUT    /person/<id>    — Update a person
  DELETE /person/<id>    — Delete a person
"""

import sqlite3
import json
from functools import wraps
from flask import Flask, request, jsonify, g
from jsonschema import validate, ValidationError

app = Flask(__name__)

DATABASE = "people.db"

# ---------------------------------------------------------------------------
# JSON Schemas
# ---------------------------------------------------------------------------

CREATE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100,
            "description": "First name",
        },
        "last_name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100,
            "description": "Last name",
        },
        "id_number": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50,
            "description": "ID number (e.g. national ID, passport, etc.)",
        },
    },
    "required": ["name", "last_name", "id_number"],
    "additionalProperties": False,
}

UPDATE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1, "maxLength": 100},
        "last_name": {"type": "string", "minLength": 1, "maxLength": 100},
        "id_number": {"type": "string", "minLength": 1, "maxLength": 50},
    },
    "additionalProperties": False,
    "minProperties": 1,
}


# ---------------------------------------------------------------------------
# Validation decorator
# ---------------------------------------------------------------------------

def validate_json(schema):
    """Decorator that validates the incoming JSON body against a schema."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True)
            if data is None:
                return jsonify({"error": "Request body must be valid JSON."}), 400
            try:
                validate(instance=data, schema=schema)
            except ValidationError as exc:
                return jsonify({"error": exc.message}), 400
            return f(data, *args, **kwargs)
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    """Create the table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS person (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT    NOT NULL,
            last_name TEXT    NOT NULL,
            id_number TEXT    NOT NULL UNIQUE
        )
        """
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Routes — CRUD
# ---------------------------------------------------------------------------

@app.route("/person", methods=["POST"])
@validate_json(CREATE_SCHEMA)
def create_person(data):
    """CREATE — add a new person."""
    db = get_db()
    try:
        db.execute(
            "INSERT INTO person (name, last_name, id_number) VALUES (?, ?, ?)",
            (data["name"], data["last_name"], data["id_number"]),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "A person with that id_number already exists."}), 409

    person_id = db.execute(
        "SELECT last_insert_rowid()"
    ).fetchone()[0]
    person = db.execute(
        "SELECT * FROM person WHERE id = ?", (person_id,)
    ).fetchone()
    return jsonify(dict(person)), 201


@app.route("/person", methods=["GET"])
def list_people():
    """READ (all) — list every person."""
    db = get_db()
    rows = db.execute("SELECT * FROM person ORDER BY id").fetchall()
    return jsonify([dict(r) for r in rows]), 200


@app.route("/person/<int:person_id>", methods=["GET"])
def get_person(person_id):
    """READ (one) — get a single person by database ID."""
    db = get_db()
    row = db.execute("SELECT * FROM person WHERE id = ?", (person_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Person not found."}), 404
    return jsonify(dict(row)), 200


@app.route("/person/<int:person_id>", methods=["PUT"])
@validate_json(UPDATE_SCHEMA)
def update_person(data, person_id):
    """UPDATE — modify an existing person (partial update allowed)."""
    db = get_db()
    row = db.execute("SELECT * FROM person WHERE id = ?", (person_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Person not found."}), 404

    # Merge existing values with the ones provided
    merged = {
        "name": data.get("name", row["name"]),
        "last_name": data.get("last_name", row["last_name"]),
        "id_number": data.get("id_number", row["id_number"]),
    }

    try:
        db.execute(
            "UPDATE person SET name = ?, last_name = ?, id_number = ? WHERE id = ?",
            (merged["name"], merged["last_name"], merged["id_number"], person_id),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "That id_number is already in use."}), 409

    updated = db.execute("SELECT * FROM person WHERE id = ?", (person_id,)).fetchone()
    return jsonify(dict(updated)), 200


@app.route("/person/<int:person_id>", methods=["DELETE"])
def delete_person(person_id):
    """DELETE — remove a person."""
    db = get_db()
    row = db.execute("SELECT * FROM person WHERE id = ?", (person_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Person not found."}), 404

    db.execute("DELETE FROM person WHERE id = ?", (person_id,))
    db.commit()
    return jsonify({"message": "Person deleted.", "person": dict(row)}), 200


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)