# scripts/reflex_correction_engine.py

import json
from datetime import datetime
from pathlib import Path

DRIFT_LOG = Path("memory/reflex_drift_log.json")
WEIGHT_LOG = Path("memory/reflex_weight_log.json")
CORRECTION_LOG = Path("memory/reflex_correction_log.json")

CORRECTION_FACTOR = 0.5  # Tuneable factor

def load_json(path):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def main():
    print("🔧 Reflex Correction Engine Running...")

    drift_entries = load_json(DRIFT_LOG)
    weight_map = load_json(WEIGHT_LOG)
    corrections = []

    for entry in drift_entries:
        reflex = entry["reflex"]
        drift = entry["drift"]

        if abs(drift) < 0.1:
            continue  # Ignore minor drift

        if reflex not in weight_map:
            continue

        old_weight = weight_map[reflex]
        correction = -drift * CORRECTION_FACTOR
        new_weight = round(old_weight + correction, 3)

        weight_map[reflex] = new_weight

        corrections.append({
            "timestamp": datetime.utcnow().isoformat(),
            "reflex": reflex,
            "old_weight": old_weight,
            "drift": drift,
            "correction_applied": correction,
            "new_weight": new_weight
        })

        print(f"[CORRECT] Reflex '{reflex}' adjusted by {correction} → New weight: {new_weight}")

    # Save updates
    save_json(WEIGHT_LOG, weight_map)

    if corrections:
        if CORRECTION_LOG.exists():
            existing = load_json(CORRECTION_LOG)
        else:
            existing = []
        existing.extend(corrections)
        save_json(CORRECTION_LOG, existing)

if __name__ == "__main__":
    main()
