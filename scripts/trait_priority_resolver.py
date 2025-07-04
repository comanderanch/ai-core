import json
from pathlib import Path
from datetime import datetime

# Paths
PRIORITY_MAP_PATH = Path("memory/trait_priority_map.json")
ANCHOR_MAP_PATH = Path("memory/trait_anchor_stability_map.json")
DRIFT_MAP_PATH = Path("memory/trait_influence_log.json")
OUTPUT_PATH = Path("memory/trait_priority_resolution.json")

def load_json(path, fallback):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return fallback
    return fallback

def resolve_conflicts(priority_scores, anchors, drift_data):
    """
    Resolve conflicts between traits with identical priority scores
    using fallback criteria:
      1. Higher stability_score
      2. Lower drift magnitude
      3. Alphabetical order
    """
    grouped = {}
    for trait_id, score in priority_scores.items():
        grouped.setdefault(score, []).append(trait_id)

    resolved = {}

    for score, traits in grouped.items():
        if len(traits) == 1:
            resolved[traits[0]] = score
            continue

        # Resolve by fallback logic
        def fallback_sort_key(trait_id):
            stability = anchors.get("anchors", {}).get(trait_id, {}).get("stability_score", 0.0)
            drift = drift_data.get("influence", {}).get(trait_id, {}).get("magnitude", 1.0)
            return (-stability, drift, trait_id)  # Higher stability, lower drift, alphabetical

        sorted_traits = sorted(traits, key=fallback_sort_key)
        for idx, tid in enumerate(sorted_traits):
            resolved[tid] = round(score - (idx * 0.001), 6)  # Slightly reduce to preserve order

    return resolved

def main():
    print("🧮 Resolving Trait Priority Conflicts...")

    priority_map = load_json(PRIORITY_MAP_PATH, {}).get("priority_scores", {})
    anchor_map = load_json(ANCHOR_MAP_PATH, {})
    drift_map = load_json(DRIFT_MAP_PATH, {})

    if not priority_map:
        print("[RESOLVE] No priority data found. Resolution skipped.")
        return

    resolved = resolve_conflicts(priority_map, anchor_map, drift_map)

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "resolved_priorities": resolved
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[RESOLVE] Trait priorities resolved for {len(resolved)} traits.")

if __name__ == "__main__":
    main()
