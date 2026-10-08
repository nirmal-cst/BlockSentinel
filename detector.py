def detect_threat(event_type, details):
    text = f"{event_type} {details}".lower()

    if any(x in text for x in ["sql injection", "union select", "drop table", "' or 1=1"]):
        return {"threat": "YES", "severity": "CRITICAL",
                "status": "SQL Injection Detected"}
    if any(x in text for x in ["port scan", "nmap", "scan detected"]):
        return {"threat": "YES", "severity": "HIGH",
                "status": "Port Scan Detected"}
    if "failed login" in text:
        import re
        nums = re.findall(r"\d+", text)
        attempts = int(nums[-1]) if nums else 1
        if attempts >= 5:
            return {"threat": "YES", "severity": "HIGH",
                    "status": "Brute Force Detected"}
        if attempts >= 3:
            return {"threat": "YES", "severity": "MEDIUM",
                    "status": "Suspicious Login Activity"}
    if "unknown ip" in text or "unknown device" in text:
        return {"threat": "YES", "severity": "MEDIUM",
                "status": "Suspicious Source"}
    return {"threat": "NO", "severity": "LOW", "status": "Normal Event"}
