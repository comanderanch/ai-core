# scripts/trait_memory_unifier.py

import json
from pathlib import Path
from datetime import datetime

# Input paths
MEMORY_PATH = Path("memory/trait_memory_log.json")
FEEDBACK_PATH = Path("memory/trait_feedback_log.json")
INFLUENCE_PATH = Path("memory/trait_influence_log.json")
DRIFT_SUMMARY_PATH = Path("memory/trait_drift_summary.json")
ANCHOR_PATH = Path("memory/trait_anchor_stability_map.json")
CLUSTER_PATH = Path("memory/trait_cluster_map.json")

# Output path
MASTER_LOG_PATH = Path("memory/trait_master_log.json")

def load_json(path, fallback):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return fallback
    return fallback

def unify_trait_data():
    memory_entries = load_json(MEMORY_PATH, [])
    feedback_data = load_json(FEEDBACK_PATH, {}).get("feedback", {})
    influence_data = load_json(INFLUENCE_PATH, {}).get("influence", {})
    drift_summary = load_json(DRIFT_SUMMARY_PATH, {}).get("summary", {})
    anchor_data = load_json(ANCHOR_PATH, {}).get("anchors", {})
    cluster_data = load_json(CLUSTER_PATH, {}).get("clusters", {})

    unified = {}

    for entry in memory_entries:
        trait_id = entry["trait_id"]
        unified[trait_id] = {
            "label": entry["label"],
            "reflex": entry["reflex"],
            "trait": entry["trait"],
            "bias": entry["bias"],
            "weight": entry["weight"],
            "feedback": feedback_data.get(trait_id, {}),
            "influence": influence_data.get(trait_id, {}),
            "drift_summary": drift_summary.get(trait_id, {}),
            "anchor": anchor_data.get(trait_id, {}),
            "cluster": []
        }

    for cluster_id, traits in cluster_data.items():
        for trait in traits:
            for trait_id in unified:
                if unified[trait_id]["trait"] == trait:
                    unified[trait_id]["cluster"].append(cluster_id)

    return unified

def main():
    print("🔄 Unifying Trait Memory...")
    master_data = unify_trait_data()

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "unified_traits": master_data
    }

    with open(MASTER_LOG_PATH, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[UNIFY] Master trait log created with {len(master_data)} entries.")

if __name__ == "__main__":
    main()
