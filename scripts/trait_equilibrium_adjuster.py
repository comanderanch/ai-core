# scripts/trait_equilibrium_adjuster.py

import json
from pathlib import Path
from datetime import datetime

# Paths
EQUILIBRIUM_PATH = Path("memory/trait_equilibrium_summary.json")
MASTER_LOG_PATH = Path("memory/trait_master_log.json")
ADJUSTMENT_LOG_PATH = Path("memory/trait_equilibrium_adjustments.json")

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

def adjust_weight(current_weight, equilibrium_score):
    if equilibrium_score > 0.8:
        return round(current_weight + 0.01, 3)
    elif equilibrium_score < 0.2:
        return round(current_weight - 0.01, 3)
    return current_weight

def main():
    print("⚖️  Adjusting Trait Equilibrium Weights...")

    equilibrium_data = load_json(EQUILIBRIUM_PATH, {}).get("equilibrium_scores", {})
    master_log = load_json(MASTER_LOG_PATH, {}).get("unified_traits", {})
    adjustment_log = []

    for trait_id, eq_score in equilibrium_data.items():
        if trait_id in master_log:
            entry = master_log[trait_id]
            old_weight = entry.get("weight", 0.0)
            new_weight = adjust_weight(old_weight, eq_score)

            if new_weight != old_weight:
                entry["weight"] = new_weight
                adjustment_log.append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "trait_id": trait_id,
                    "old_weight": old_weight,
                    "new_weight": new_weight,
                    "equilibrium_score": eq_score
                })

    # Save updated master log
    save_json(MASTER_LOG_PATH, {
        "timestamp": datetime.utcnow().isoformat(),
        "unified_traits": master_log
    })

    # Save adjustment log
    if adjustment_log:
        save_json(ADJUSTMENT_LOG_PATH, adjustment_log)
        print(f"[ADJUST] {len(adjustment_log)} trait(s) adjusted.")
    else:
        print("[ADJUST] No traits required adjustment.")

if __name__ == "__main__":
    main()
