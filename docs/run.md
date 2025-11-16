# How to run the program

## Install
```bash
sudo apt install python3 python3-venv gcc libssl-dev sqlite3
```

## Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Compile the C core
```bash
cd c_core/
gcc -fPIC -shared -o ledger.so ledger.c -lcrypto
```

## Initialize database
```bash
cd database
sqlite3 ledger.db < schema.sql
```

## Run Flask
```bash
cd flask_app
flask run
```

## Open browser
http://127.0.0.1:5000

