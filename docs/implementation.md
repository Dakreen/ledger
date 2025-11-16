# **Implementation Overview**

## **1. What the ledger does**

The ledger records manual audit events and stores them in an **append-only**, **tamper-evident** database.
Once an event is added:

* It cannot be modified.
* It cannot be deleted without detection (except the last event — limitation of Phase 1).
* The integrity of all events can be verified at any time.

This provides a simple but strong audit trail.

---

## **2. How hashing works (C Layer)**

Hashing is handled by the function `compute_hash()` in `ledger.c`.

### **Process**

1. The function receives a **string input** representing an event’s data.
2. It allocates **65 bytes**:

   * 64 characters for the hexadecimal representation of SHA-256.
   * 1 byte for the null terminator `\0`.
3. It creates a **32-byte binary buffer** (`digest`) to store the raw SHA-256 output.
4. The OpenSSL function `SHA256()` fills `digest`.
5. Each byte of `digest` is converted into two hexadecimal characters.
6. The final readable hash (64 hex chars + `\0`) is returned.

**Why 64 hex characters?**
SHA-256 = 256 bits = 32 bytes → 32 bytes × 2 hex digits per byte → **64 hex characters**.

---

## **3. How events are chained**

Every event contains:

* `prev_hash` → the hash of the previous event
* `hash` → the hash of its own content

For the first event, `prev_hash = "GENESIS"`.

This creates a backward-linked chain:

```
Event1.hash → Event2.prev_hash
Event2.hash → Event3.prev_hash
…
```

Changing any record breaks the chain.

---

## **4. How verification detects tampering**

Tampering is detected in two ways:

### **A. Record integrity**

The C function `verify_hash()` recomputes the hash of each event:

```
verify_hash(recomputed_value, stored_hash)
```

If the two hashes differ → the record was modified.

### **B. Chain integrity**

Python (app.py):

1. Recomputes the hash of record *i−1*
2. Compares it to `prev_hash` of record *i*

If they do not match → the event chain is broken.

### **C. Missing record detection**

Using the `ledger_meta` table:

* `total_events` is updated on every insertion.
* `/verify` compares:

  * actual number of rows in `events`
  * expected number in `ledger_meta`

If mismatched → a deletion occurred.

### **Results**

* `tampered_records`: list of record IDs that failed integrity
* `missing_records`: number of deleted events
* `verified`: true/false

---

## **5. What the dashboard provides**

A single responsive page with three sections:

### **A. Add Event**

* Fields: actor, action, details
* Submit button
* Displays success or error message

### **B. Event List**

* Table with: ID, actor, action, hash
* Requires clicking “Refresh” to load events

### **C. Verify Chain**

* “Run” button
* Shows one of:

  * Chain verified
  * Tampering detected
  * Missing events detected

---

## **6. How Python, C, SQLite, and JavaScript work together**

### **C Layer (ledger.so)**

* Compiled as a shared library
* Functions exposed to Python with `ctypes`
* `compute_hash` returns a pointer (`c_void_p`)
* `free_buffer` frees allocated memory

### **Python Layer (Flask)**

* Loads `ledger.so`
* Defines argument/return types
* Calls C functions with `.encode()` / `.decode()` and `string_at()`
* Stores events in SQLite via `db.py`

### **Database Layer (db.py)**

* Handles:

  * inserting events
  * reading events
  * counting events
  * accessing metadata
* Uses parameterized SQL (safe from injection)

### **Frontend (script.js)**

* Sends form data to `/add`
* Fetches `/events` and `/verify`
* Updates the dashboard dynamically

---

## **7. Event flow**

1. User submits:

   * actor
   * action
   * details
2. Flask:

   * gets timestamp
   * fetches `prev_hash`
   * concatenates fields into one string
3. String is passed to C `compute_hash()`
4. Resulting hash is stored in SQLite with all event fields
5. Metadata table is updated (last hash + event count)
6. Event can now be displayed or verified
