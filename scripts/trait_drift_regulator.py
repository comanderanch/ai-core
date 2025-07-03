# scripts/trait_drift_regulator.py

import json
from pathlib import Path
from datetime import datetime

# File paths
DRIFT_LOG_PATH = Path("memory/trait_drift_log.json")
CORRECTION_LOG_PATH = Path("memory/trait_drift_corrections.json")

# Configurable drift threshold
DRIFT_THRESHOLD = 0.1  # Adjust if needed
MAX_CORRECTION = 0.05  # Maximum allowed correction per run

def load_json(path, fallback):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return fallback
    return fallback

def regulate_drift(drift_entries):
    corrections = []

    for entry in drift_entries:
        drift = abs(entry.get("drift", 0.0))
        if drift > DRIFT_THRESHOLD:
            adjustment = min(drift - DRIFT_THRESHOLD, MAX_CORRECTION)
            direction = -1 if entry["weight"] > entry["bias"] else 1
            corrected_weight = round(entry["weight"] + direction * adjustment, 4)

            corrections.append({
                "timestamp": datetime.utcnow().isoformat(),
                "trait_id": f"{entry['label']}:{entry['reflex']}:{entry['trait']}",
                "label": entry["label"],
                "reflex": entry["reflex"],
                "trait": entry["trait"],
                "original_weight": entry["weight"],
                "bias": entry["bias"],
                "adjustment": round(direction * adjustment, 4),
                "corrected_weight": corrected_weight
            })

    return corrections

def main():
    print("🧪 Running Trait Drift Regulator...")

    drift_entries = load_json(DRIFT_LOG_PATH, [])
    if not drift_entries:
        print("[DRIFT-REG] No drift data found. Regulation skipped.")
        return

    corrections = regulate_drift(drift_entries)

    if not corrections:
        print("[DRIFT-REG] No corrections needed.")
        return

    # Save corrections
    with open(CORRECTION_LOG_PATH, "w") as f:
        json.dump(corrections, f, indent=4)

    print(f"[DRIFT-REG] {len(corrections)} correction(s) written to {CORRECTION_LOG_PATH.name}")

if __name__ == "__main__":
    main()
