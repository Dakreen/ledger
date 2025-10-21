# Ledger – CS50 Final Project (Phase 1)

## Purpose
Ledger is a cybersecurity audit system that records and verifies system events using a **tamper-evident hash chain**.  
Each event links to the previous one, ensuring **immutability** and **integrity**.

## Tech Stack
- **C** – Core hashing and verification logic  
- **Flask** – Web interface and API layer  
- **SQLite** – Local data storage

## Core Features
- Add, view, and verify events  
- Generate and validate hash-chain integrity  
- Detect and report tampering  
- Simple local dashboard for demonstration

## Security Model
- **Append-only:** events cannot be modified or deleted  
- **Validated input:** Flask checks all data before saving  
- **Integrity check:** each hash depends on the previous one  
- **Tamper detection:** any change breaks the chain and is flagged  

## Usage
1. Run the Flask app locally.  
2. Open the dashboard in your browser.  
3. Add a few events.  
4. Use the “Verify Chain” button to check integrity.  
5. Modify one record manually to simulate tampering — Ledger will detect it.

## Goal
Demonstrate cybersecurity integrity principles for **CS50 final evaluation**,  
and prepare for **Phase 2 (Azure Deployment + Post-Quantum Security)**.
