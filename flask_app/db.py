from flask import g
import sqlite3

def get_db_connection():
    if "db" not in g:
        g.db = sqlite3.connect("../database/ledger.db")
        g.db.row_factory = sqlite3.Row
    return g.db

def insert_event(timestamp, actor, action, details, prev_hash, hash):
    db = get_db_connection()
    db.execute(
        """
        INSERT INTO events(timestamp, actor, action, details, prev_hash, hash)
        VALUES(?, ?, ?, ?, ?, ?)
        """, (timestamp, actor, action, details, prev_hash, hash)
    )
    db.commit()

def get_all_events():
    db = get_db_connection()
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
    db = get_db_connection()
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

def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()