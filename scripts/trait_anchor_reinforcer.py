# scripts/trait_anchor_reinforcer.py

import json
from pathlib import Path
from datetime import datetime

# Paths
ANCHOR_MAP_PATH = Path("memory/trait_anchor_stability_map.json")
MASTER_LOG_PATH = Path("memory/trait_master_log.json")
REINFORCEMENT_LOG = Path("memory/trait_anchor_reinforcement_log.json")

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

def reinforce_anchors(master_log, anchor_map):
    reinforced = []

    anchors = anchor_map.get("anchors", {})
    for trait_id, anchor_data in anchors.items():
        stability = anchor_data.get("stability_score", 0.0)
        if stability >= 0.85:
            if trait_id in master_log["unified_traits"]:
                trait_data = master_log["unified_traits"][trait_id]
                old_weight = trait_data["weight"]
                new_weight = round(old_weight + 0.05, 4)
                trait_data["weight"] = new_weight

                reinforced.append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "trait_id": trait_id,
                    "old_weight": old_weight,
                    "new_weight": new_weight,
                    "stability_score": stability
                })

    return reinforced

def main():
    print("🪝 Reinforcing Anchored Traits...")

    master_log = load_json(MASTER_LOG_PATH, {})
    anchor_map = load_json(ANCHOR_MAP_PATH, {})
    reinforcement_log = load_json(REINFORCEMENT_LOG, [])

    if not master_log or "unified_traits" not in master_log:
        print("[ANCHOR-REINFORCE] No valid master trait data found.")
        return

    reinforced = reinforce_anchors(master_log, anchor_map)

    if reinforced:
        save_json(MASTER_LOG_PATH, master_log)
        reinforcement_log.extend(reinforced)
        save_json(REINFORCEMENT_LOG, reinforcement_log)
        print(f"[ANCHOR-REINFORCE] {len(reinforced)} trait(s) reinforced.")
    else:
        print("[ANCHOR-REINFORCE] No traits qualified for reinforcement.")

if __name__ == "__main__":
    main()
