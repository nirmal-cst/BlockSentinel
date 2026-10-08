from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime
from blockchain import Blockchain
from detector import detect_threat

app = Flask(__name__)
DB = "blocksentinel.db"
chain = Blockchain()

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, event_type TEXT, ip TEXT, details TEXT,
        status TEXT, severity TEXT, threat TEXT
    )""")
    conn.commit()
    conn.close()

def add_event(event_type, ip, details):
    result = detect_threat(event_type, details)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "timestamp": timestamp, "event_type": event_type, "ip": ip,
        "details": details, "status": result["status"],
        "severity": result["severity"], "threat": result["threat"]
    }
    block = chain.add_block(data)
    conn = get_db()
    conn.execute("""INSERT INTO events
        (timestamp,event_type,ip,details,status,severity,threat)
        VALUES (?,?,?,?,?,?,?)""",
        (timestamp,event_type,ip,details,result["status"],
         result["severity"],result["threat"]))
    conn.commit()
    conn.close()
    return result, block

@app.route("/")
def dashboard():
    conn = get_db()
    rows = conn.execute("SELECT * FROM events ORDER BY id DESC LIMIT 10").fetchall()
    stats = {
        "events": conn.execute("SELECT COUNT(*) FROM events").fetchone()[0],
        "threats": conn.execute("SELECT COUNT(*) FROM events WHERE threat='YES'").fetchone()[0],
        "critical": conn.execute("SELECT COUNT(*) FROM events WHERE severity='CRITICAL'").fetchone()[0],
    }
    conn.close()
    return render_template("dashboard.html", events=rows, stats=stats,
                           blocks=len(chain.chain), valid=chain.is_valid())

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        event_type = request.form.get("event_type","Normal Login")
        ip = request.form.get("ip","127.0.0.1")
        details = request.form.get("details","")
        result, block = add_event(event_type, ip, details)
        return render_template("result.html", result=result, block=block)
    return render_template("add_event.html")

@app.route("/blockchain")
def blockchain():
    return render_template("blockchain.html", chain=chain.chain,
                           valid=chain.is_valid())

@app.route("/verify")
def verify():
    return jsonify({"valid": chain.is_valid(), "blocks": len(chain.chain)})

@app.route("/api/events")
def api_events():
    conn = get_db()
    rows = [dict(r) for r in conn.execute(
        "SELECT * FROM events ORDER BY id DESC LIMIT 50").fetchall()]
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
