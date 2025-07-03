# scripts/reflex_reinforcement_trainer.py

import json
from datetime import datetime
from pathlib import Path

INFLUENCE_FILE = "memory/reflex_influence_summary.json"
WEIGHT_FILE = "memory/reflex_weight_log.json"
REINFORCEMENT_LOG = "memory/reflex_reinforcement_log.json"

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def reinforce():
    influence_data = load_json(INFLUENCE_FILE)
    weight_data = load_json(WEIGHT_FILE)
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "reinforced": []
    }

    for reflex, influence_count in influence_data.items():
        weight = weight_data.get(reflex, 1.0)
        adjusted_weight = round(weight + (influence_count * 0.05), 3)
        weight_data[reflex] = adjusted_weight
        log_entry["reinforced"].append({
            "reflex": reflex,
            "original_weight": weight,
            "new_weight": adjusted_weight,
            "count": influence_count
        })

    save_json(WEIGHT_FILE, weight_data)

    if Path(REINFORCEMENT_LOG).exists():
        log = load_json(REINFORCEMENT_LOG)
        log.append(log_entry)
    else:
        log = [log_entry]

    save_json(REINFORCEMENT_LOG, log)
    print(f"[REINFORCE] Reinforcement complete: {len(log_entry['reinforced'])} reflexes updated.")

if __name__ == "__main__":
    reinforce()
