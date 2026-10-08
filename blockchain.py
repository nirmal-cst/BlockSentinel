import hashlib
import json
from datetime import datetime

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis()

    def create_genesis(self):
        self.add_block({"event": "Genesis Block", "status": "SYSTEM"})

    def calculate_hash(self, block):
        content = json.dumps(block, sort_keys=True, default=str).encode()
        return hashlib.sha256(content).hexdigest()

    def add_block(self, data):
        previous_hash = self.chain[-1]["hash"] if self.chain else "0" * 64
        block = {
            "index": len(self.chain),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "data": data,
            "previous_hash": previous_hash
        }
        block["hash"] = self.calculate_hash(block)
        self.chain.append(block)
        return block

    def is_valid(self):
        for i, block in enumerate(self.chain):
            if block["hash"] != self.calculate_hash({
                "index": block["index"],
                "timestamp": block["timestamp"],
                "data": block["data"],
                "previous_hash": block["previous_hash"]
            }):
                return False
            if i > 0 and block["previous_hash"] != self.chain[i-1]["hash"]:
                return False
        return True
