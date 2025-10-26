from flask import Flask, request, jsonify
from ctypes import CDLL, c_char_p, c_int
from datetime import datetime, timezone
from db import insert_event, get_all_events, get_last_event, close_db
import os

# Initialize Flask
app = Flask(__name__)
app.teardown_appcontext(close_db)

# Locate and load the compiled C library
base_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(base_dir, "../c_core/ledger.so")
lib = CDLL(lib_path)

# Configure return types from C
lib.compute_hash.restype = c_char_p
lib.verify_hash.restype = c_int


# --- ROUTES --------------------------------------------------

@app.route("/")
def index():
    return jsonify({"message": "Ledger API active"})


@app.route("/add", methods=["POST"])
def add_event():
    """Add a new event to the ledger."""
    data = request.get_json()
    # check input
    if not data["actor"]:
        return jsonify({"error": "no data"}), 400
    if len(data["actor"]) > 50:
        return jsonify({"error":"actor input too long"}), 400
    if not data["action"]:
        return jsonify({"error": "no action"}), 400
    if len(data["action"]) > 50:
        return jsonify({"error":"action input too long"}), 400
    if not data["details"]:
        return jsonify({"error": "no data"}), 400
    if len(data["details"]) > 50:
        return jsonify({"error":"data too long"}), 400
    # compute hash
    timestamp = datetime.now(timezone.utc).isoformat()
    prev_hash = get_last_event()
    data_output = timestamp + data["actor"] + data["action"] + data["details"] + prev_hash
    hash_bytes = lib.compute_hash(data_output.encode())
    hash = hash_bytes.decode()
    # insert into database
    insert_event(timestamp, data["actor"], data["action"], data["details"], prev_hash, hash)

    return jsonify({
        "status": "ok", 
        "hash": hash,
        "prev_hash": prev_hash
    })


@app.route("/events", methods=["GET"])
def list_events():
    """List all events."""
    data = get_all_events()

    return jsonify({"status": "ok", "events": data})


@app.route("/verify", methods=["GET"])
def verify_chain():
    """Verify ledger integrity"""
    data = get_all_events()
    tampered = []

    for i in range(0, len(data)):
        # recompute integrity
        output = data[i]["timestamp"] + data[i]["actor"] + data[i]["action"] + data[i]["details"] + data[i]["prev_hash"]
        hash_bytes = lib.compute_hash(output.encode())
        hash = hash_bytes.decode()
        if hash != data[i]["hash"]:
            tampered.append(data[i]["id"])

        # check chain integrity
        if i > 0 and data[i]["prev_hash"] != data[i - 1]["hash"]:
            tampered.append(data[i]["id"])

    if not tampered:
        return jsonify({"status": "ok", "verified": True, "tampered_records": []})    
    else:
        return jsonify({"status": "ok", "verified": False, "tampered_records": tampered})


# --- MAIN ENTRY ----------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
