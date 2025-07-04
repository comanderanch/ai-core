# scripts/trait_anchor_stability_mapper.py

import json
from pathlib import Path
from datetime import datetime

# Paths
TRAIT_LOG_PATH = Path("memory/trait_memory_log.json")
OUTPUT_PATH = Path("memory/trait_anchor_stability_map.json")

def load_json(path, fallback):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return fallback
    return fallback

def map_anchor_stability(trait_log):
    anchor_map = {}

    for entry in trait_log:
        trait_id = entry.get("trait_id")
        label = entry.get("label")
        reflex = entry.get("reflex")
        trait = entry.get("trait")
        bias = entry.get("bias", 0.0)
        weight = entry.get("weight", 0.0)

        stability = round(1.0 - abs(bias - weight), 4)

        anchor_map[trait_id] = {
            "label": label,
            "reflex": reflex,
            "trait": trait,
            "bias": bias,
            "weight": weight,
            "stability_score": stability
        }

    return anchor_map

def main():
    print("📌 Mapping Trait Anchor Stability...")

    trait_log = load_json(TRAIT_LOG_PATH, [])

    if not trait_log:
        print("[ANCHOR] No trait memory data found. Mapping skipped.")
        return

    anchor_map = map_anchor_stability(trait_log)

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "anchors": anchor_map
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[ANCHOR] {len(anchor_map)} trait anchors mapped.")

if __name__ == "__main__":
    main()
