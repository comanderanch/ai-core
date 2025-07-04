# scripts/trait_drift_reinforcer.py

import json
from datetime import datetime
from pathlib import Path

DRIFT_LOG = Path("memory/trait_drift_log.json")
WEIGHT_LOG = Path("memory/reflex_weight_log.json")
OUTPUT_LOG = Path("memory/trait_drift_reinforcement_log.json")

def load_json(path, fallback):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return fallback
    return fallback

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def reinforce_drift(drift_log, weight_map):
    reinforcement_log = []
    for entry in drift_log:
        reflex = entry["reflex"]
        drift = entry["drift"]
        current_weight = weight_map.get(reflex, 1.0)

        # Determine reinforcement or suppression
        if drift > 0.05:
            new_weight = round(current_weight + 0.05, 3)
            action = "reinforced"
        elif drift < -0.05:
            new_weight = round(current_weight - 0.05, 3)
            action = "suppressed"
        else:
            continue  # Skip small drift

        # Apply update
        weight_map[reflex] = new_weight
        reinforcement_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "reflex": reflex,
            "action": action,
            "old_weight": current_weight,
            "new_weight": new_weight,
            "drift": drift
        })

    return weight_map, reinforcement_log

def main():
    print("🔁 Running Trait Drift Reinforcer...")

    drift_log = load_json(DRIFT_LOG, [])
    weight_map = load_json(WEIGHT_LOG, {})
    reinforcement_log = load_json(OUTPUT_LOG, [])

    if not drift_log:
        print("[DRIFT-REG] No drift data found. Reinforcement skipped.")
        return

    updated_weights, new_log_entries = reinforce_drift(drift_log, weight_map)

    # Save updated weights and reinforcement history
    save_json(WEIGHT_LOG, updated_weights)
    reinforcement_log.extend(new_log_entries)
    save_json(OUTPUT_LOG, reinforcement_log)

    print(f"[DRIFT-REG] {len(new_log_entries)} reflex weights updated due to drift.")

if __name__ == "__main__":
    main()
