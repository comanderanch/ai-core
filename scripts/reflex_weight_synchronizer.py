# scripts/reflex_weight_synchronizer.py

import json
from datetime import datetime
from pathlib import Path

# File paths
WEIGHT_LOG = Path("memory/reflex_weight_log.json")
SYNC_LOG = Path("memory/reflex_weight_sync_log.json")

def load_weights():
    if WEIGHT_LOG.exists():
        with open(WEIGHT_LOG, "r") as f:
            return json.load(f)
    return {}

def main():
    print("🔄 Synchronizing Reflex Weights...")

    weights = load_weights()
    timestamp = datetime.utcnow().isoformat()

    sync_record = {
        "timestamp": timestamp,
        "weights": weights
    }

    # Append to sync log
    if SYNC_LOG.exists():
        with open(SYNC_LOG, "r") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []
    else:
        existing = []

    existing.append(sync_record)

    with open(SYNC_LOG, "w") as f:
        json.dump(existing, f, indent=4)

    print(f"[SYNC] {len(weights)} reflex weights recorded at {timestamp}")

if __name__ == "__main__":
    main()
