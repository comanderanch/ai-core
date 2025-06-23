# scripts/legacy_thread_binder.py

import os
import json
import datetime

LEGACY_THREAD_PATH = "memory/legacy_threads/"
DOCTRINE_FILE = "memory/sensory/sensory_mapping_output.json"
BIND_OUTPUT_FILE = "memory/thread_binds/legacy_thread_binds.json"

class LegacyThreadBinder:
    def __init__(self):
        self.timestamp = datetime.datetime.now().isoformat()
        self.threads = []

    def load_doctrine_data(self):
        if not os.path.exists(DOCTRINE_FILE):
            raise FileNotFoundError(f"Doctrine file not found: {DOCTRINE_FILE}")
        with open(DOCTRINE_FILE, "r") as f:
            return json.load(f)

    def bind_threads(self, doctrine_data):
        for item in doctrine_data.get("sensory_links", []):
            thread = {
                "origin": item.get("source_id", "unknown"),
                "type": item.get("type", "unspecified"),
                "mapped_token": item.get("token", ""),
                "frequency": item.get("frequency", 0),
                "bound_at": self.timestamp
            }
            self.threads.append(thread)

    def save_binds(self):
        os.makedirs(os.path.dirname(BIND_OUTPUT_FILE), exist_ok=True)
        with open(BIND_OUTPUT_FILE, "w") as f:
            json.dump({"thread_binds": self.threads}, f, indent=4)

    def run(self):
        doctrine_data = self.load_doctrine_data()
        self.bind_threads(doctrine_data)
        self.save_binds()
        print(f"[{self.timestamp}] Legacy threads bound and saved.")

if __name__ == "__main__":
    binder = LegacyThreadBinder()
    binder.run()
