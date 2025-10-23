from flask import Flask, request, jsonify
from ctypes import CDLL, c_char_p, c_int
import os

# Initialize Flask
app = Flask(__name__)

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
    if data["actor"] is not None:
        ""
    return jsonify({"status": "pending", "route": "/add"})


@app.route("/events", methods=["GET"])
def list_events():
    """List all events (to be implemented)."""
    return jsonify({"status": "pending", "route": "/events"})


@app.route("/verify", methods=["GET"])
def verify_chain():
    """Verify ledger integrity (to be implemented)."""
    return jsonify({"status": "pending", "route": "/verify"})


# --- MAIN ENTRY ----------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
