import os

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql:///catdb")
FIELDS = ["name", "breed", "age", "gender", "color", "owner_name", "owner_phone"]

app = Flask(__name__, static_folder="static", static_url_path="")


def get_conn():
    return psycopg2.connect(DATABASE_URL)


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/cats")
def list_cats():
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM cat.family ORDER BY id DESC")
        rows = cur.fetchall()
    for row in rows:
        row["created_at"] = row["created_at"].isoformat(sep=" ", timespec="seconds")
    return jsonify(rows)


@app.post("/api/cats")
def create_cat():
    data = request.get_json(silent=True) or {}
    values = {f: (str(data.get(f) or "").strip() or None) for f in FIELDS}

    errors = []
    if not values["name"]:
        errors.append("Cat name is required.")
    if not values["owner_name"]:
        errors.append("Owner name is required.")
    if values["age"] is not None:
        if not values["age"].isdigit():
            errors.append("Age must be a whole number.")
        else:
            values["age"] = int(values["age"])
    if values["gender"] not in (None, "Male", "Female"):
        errors.append("Gender must be Male or Female.")
    if errors:
        return jsonify({"errors": errors}), 400

    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            f"INSERT INTO cat.family ({', '.join(FIELDS)}) "
            f"VALUES ({', '.join(['%s'] * len(FIELDS))}) RETURNING id",
            [values[f] for f in FIELDS],
        )
        new_id = cur.fetchone()["id"]
    return jsonify({"id": new_id}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)