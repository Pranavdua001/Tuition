from flask import Flask, jsonify, send_from_directory
import os
import json
import re

app = Flask(__name__)

DATA_DIR = "data"

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/auth")
def auth():
    with open(os.path.join(DATA_DIR, "auth.json")) as f:
        return jsonify(json.load(f))

@app.route("/latest-data")
def latest_data():
    files = os.listdir(DATA_DIR)
    data_files = [f for f in files if re.match(r"data_\\d+\\.json", f)]

    if not data_files:
        return jsonify({"error": "No data published yet"})

    latest = max(data_files, key=lambda x: int(re.findall(r"\\d+", x)[0]))
    return send_from_directory(DATA_DIR, latest)

if __name__ == "__main__":
    app.run(debug=True)
