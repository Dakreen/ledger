# **Ledger**

## **Purpose**

Ledger is a security auditing system that records and verifies events using a **tamper-evident hash chain**.
Each event references the hash of the previous one, ensuring **immutability**, **integrity**, and **auditability**.

## **Tech Stack**

* **C** — Core hashing and verification logic
* **Flask** — API layer and backend logic
* **SQLite** — Local, lightweight storage
* **JavaScript / Bootstrap** — Interactive dashboard UI

## **Core Features**

* Add new events through a web form
* View all recorded events
* Verify the integrity of the entire chain
* Detect and report tampered records
* Detect missing or deleted events
* Simple, responsive dashboard interface

## **Security Model**

* **Append-only:** Events cannot be modified or removed without detection
* **Hash chaining:** Every event includes the previous event’s hash (`prev_hash`)
* **Integrity validation:** Recomputes each event’s hash and compares it with the stored version
* **Chain verification:** Ensures correct linking between consecutive records
* **Deletion checks:** Uses a metadata table (`ledger_meta`) to detect missing events
* **Input validation:** Basic length and presence checks for user input

---

# **Version History**

### **v0.9.0-beta — Local Ledger**

This is the first functional beta release of the Ledger system.
It runs entirely **locally** and provides all core features of the audit chain.

#### Included in this release:

* Local execution (Flask server + SQLite DB + C shared library)
* Event insertion with basic validation (empty/length checks)
* SHA-256 hashing implemented in C (`compute_hash`, `verify_hash`)
* Fully functional hash-chain logic
* Integrity and chain verification
* Missing-event detection via `ledger_meta`
* Interactive dashboard:

  * Add Event
  * View Events
  * Verify Chain
* Clean integration between:

  * Python (backend)
  * C (hash engine)
  * SQLite (storage)
  * JavaScript (frontend)

#### Notes

This is a **beta** version: stable for local use, but not yet production-ready.
Advanced security improvements will add stronger validation, enhanced chain protection, and cloud deployment.
