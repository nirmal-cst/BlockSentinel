# BlockSentinel
### A Blockchain-Enabled Security Monitoring and Threat Detection System

A simple college mini-project demonstrating:
- Security event monitoring
- Rule-based threat detection
- SHA-256 blockchain-style tamper-evident logging
- SQLite database
- Web dashboard

## 1. Install Python
Python 3.10+ recommended.

## 2. Install dependencies
```bash
pip install -r requirements.txt
```

## 3. Run
```bash
python app.py
```

Open:
`http://127.0.0.1:5000`

## 4. Demonstration
Try these events:

### Normal
Event Type: Normal Login
Details: Successful login

### Brute Force
Event Type: Failed Login
Details: 7 failed login attempts

### SQL Injection
Event Type: Web Request
Details: SQL Injection attempt using UNION SELECT

### Port Scan
Event Type: Network
Details: Port scan detected using nmap

Then open **Blockchain Explorer** and click **Verify Blockchain**.

## Important
This is an educational prototype, not a production security monitoring system.
The blockchain is implemented as a local hash-linked ledger for demonstration.
