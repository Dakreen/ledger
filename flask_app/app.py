from flask import Flask, request, jsonify, render_template, redirect
from ctypes import CDLL, c_char_p, c_int, c_void_p, string_at
from datetime import datetime, timezone
import os, sys

# Locate and load the compiled C library
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LIB_PATH = os.path.join(BASE_DIR, "c_core", "ledger.so")
sys.path.append(BASE_DIR)
lib = CDLL(LIB_PATH)
from flask_app.db import insert_event, get_all_events, get_last_event, count_events, update_meta, get_total_events

# Initialize Flask
app = Flask(__name__)

# Configure argument types from C
lib.compute_hash.argtypes = [c_char_p]
lib.verify_hash.argtypes = [c_char_p, c_char_p]
lib.free_buffer.argtypes = [c_void_p]

# Configure return types from C
lib.compute_hash.restype = c_void_p
lib.verify_hash.restype = c_int
lib.free_buffer.restype = None


# --- ROUTES --------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add_event():
    """Add a new event to the ledger."""

    # Get input
    actor = request.form.get("actor").strip()
    action = request.form.get("event_action").strip()
    details = request.form.get("details").strip()

    # check input
    if not actor or not action or not details:
        return jsonify({"error": "All inputs must be filled"})
    if len(actor) > 50 or len(action) > 50 or len(details) > 50:
        return jsonify({"error": "All inputs must have appropriate length"})
    
    # compute hash
    timestamp = datetime.now(timezone.utc).isoformat()
    prev_hash = get_last_event()
    data_output = timestamp + actor + action + details + prev_hash
    hash_bytes = lib.compute_hash(data_output.encode())
    hash = string_at(hash_bytes).decode() # because of c_void_p return pointer and must use string_at before decode() to read content
    lib.free_buffer(hash_bytes)
    
    # insert into database
    count = count_events()
    insert_event(timestamp, actor, action, details, prev_hash, hash)
    update_meta(count + 1, hash)  

    return redirect("/")


@app.route("/events", methods=["GET"])
def list_events():
    """List all events."""
    data = get_all_events()

    return jsonify(data)


@app.route("/verify", methods=["GET"])
def verify_chain():
    """Verify ledger integrity"""
    data = get_all_events()
    tampered = []

    for i in range(0, len(data)):
        # recompute integrity
        output = data[i]["timestamp"] + data[i]["actor"] + data[i]["action"] + data[i]["details"] + data[i]["prev_hash"]
        prev_output = data[i - 1]["timestamp"] + data[i - 1]["actor"] + data[i - 1]["action"] + data[i - 1]["details"] + data[i - 1]["prev_hash"]
        if lib.verify_hash(output.encode(), data[i]["hash"].encode()) == 0:
            tampered.append(data[i]["id"])

        # check chain integrity
        if i > 0 and lib.verify_hash(prev_output.encode(), data[i]["prev_hash"].encode()) == 0:
            tampered.append(data[i]["id"])

    # check for missing events
    total_events = get_total_events()
    count = count_events()
    missing_records = total_events - count

    if not tampered:
        return jsonify({"verified": True, "tampered_records": tampered, "missing_records": missing_records})
    else:
        return jsonify({"verified": False, "tampered_records": tampered, "missing_records": missing_records})


# --- MAIN ENTRY ----------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
