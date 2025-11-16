import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "ledger.db")

def insert_event(timestamp, actor, action, details, prev_hash, hash):
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            """
            INSERT INTO events(timestamp, actor, action, details, prev_hash, hash)
            VALUES(?, ?, ?, ?, ?, ?)
            """, (timestamp, actor, action, details, prev_hash, hash)
        )

def get_all_events():
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        cursor = db.execute(
            """
            SELECT * FROM events ORDER BY id ASC
            """
        )
        rows = cursor.fetchall()
        dict_rows = []
        for r in rows:
            dict_rows.append(dict(r))
        return dict_rows

def get_last_event():
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        cursor = db.execute(
            """
            SELECT hash FROM events ORDER BY id DESC LIMIT 1
            """
        )
        row = cursor.fetchone()
        if not row:
            return "GENESIS"
        else:
            return row["hash"]
    
def count_events():
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        cursor = db.execute("SELECT COUNT(*) AS counter FROM events")
        row = cursor.fetchone()
        return row["counter"]

def update_meta(count, hash):
    with sqlite3.connect(DB_PATH) as db:
        db.execute("INSERT OR REPLACE INTO ledger_meta(id, total_events, last_hash) VALUES(1, ?, ?)", (count, hash))

def get_total_events():
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        cursor = db.execute("SELECT total_events FROM ledger_meta")
        row = cursor.fetchone()
        if row:
            return row["total_events"]
        else:
            return 0