from flask import Flask, request, jsonify, render_template, redirect
from ctypes import CDLL, c_char_p, c_int, c_void_p
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

# Configure argument types from C
lib.compute_hash.argtypes = [c_char_p]
lib.verify_hash.argtypes = [c_void_p, c_char_p]
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
    hash = hash_bytes.decode()
    lib.free_buffer(hash_bytes)
    
    # insert into database
    insert_event(timestamp, actor, action, details, prev_hash, hash)

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
        hash_bytes = lib.compute_hash(output.encode())
        if lib.verify_hash(hash_bytes, data[i]["hash"].encode()):
            tampered.append(data[i]["id"])

        # check chain integrity
        if i > 0 and lib.verify_hash(hash_bytes, data[i - 1]["hash"].encode()):
            tampered.append(data[i]["id"])

        lib.free_buffer(hash_bytes)

    if not tampered:
        return jsonify({"verified": True, "tampered_records": []})    
    else:
        return jsonify({"verified": False, "tampered_records": tampered})


# --- MAIN ENTRY ----------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
