# scripts/trait_priority_sorter.py

import json
from pathlib import Path
from datetime import datetime

# Paths
MASTER_LOG = Path("memory/trait_master_log.json")
OUTPUT_PATH = Path("memory/trait_priority_map.json")

def load_json(path, fallback):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return fallback
    return fallback

def calculate_priority_score(trait):
    # Extract components
    influence = trait.get("influence", {})
    anchor = trait.get("anchor", {})
    drift = trait.get("drift_summary", {})

    # Influence magnitude (higher = more dynamic)
    influence_score = abs(influence.get("magnitude", 0.0))

    # Anchor stability (1.0 is ideal, lower = instability)
    stability_score = 1.0 - anchor.get("stability_score", 1.0)

    # Drift magnitude (higher = more change)
    drift_score = abs(drift.get("total_drift", 0.0))

    # Composite priority score
    return round(influence_score + stability_score + drift_score, 4)

def main():
    print("📌 Sorting Trait Priorities...")

    master_log = load_json(MASTER_LOG, {})
    traits = master_log.get("unified_traits", {})

    if not traits:
        print("[PRIORITY] No unified traits found. Sorting skipped.")
        return

    priority_map = {}

    for trait_id, trait_data in traits.items():
        score = calculate_priority_score(trait_data)
        priority_map[trait_id] = score

    # Sort by score descending
    sorted_priority = dict(sorted(priority_map.items(), key=lambda x: x[1], reverse=True))

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "priority_scores": sorted_priority
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[PRIORITY] {len(sorted_priority)} traits prioritized and saved.")

if __name__ == "__main__":
    main()
