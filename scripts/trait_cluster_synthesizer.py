# scripts/trait_cluster_synthesizer.py

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Paths
TRAIT_LOG_PATH = Path("memory/trait_memory_log.json")
OUTPUT_PATH = Path("memory/trait_cluster_map.json")

# Load JSON utility
def load_json(path, fallback):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return fallback
    return fallback

# Trait clustering logic
def synthesize_clusters(trait_entries):
    clusters = defaultdict(list)

    for entry in trait_entries:
        label = entry["label"]
        reflex = entry["reflex"]
        trait = entry["trait"]
        key = f"{label}:{reflex}"

        clusters[key].append(trait)

    return clusters

def main():
    print("🔗 Synthesizing Trait Clusters...")

    trait_entries = load_json(TRAIT_LOG_PATH, [])

    if not trait_entries:
        print("[CLUSTER] No trait memory data found. Synthesis skipped.")
        return

    clusters = synthesize_clusters(trait_entries)

    output = {
        "timestamp": datetime.utcnow().isoformat(),
        "clusters": clusters
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=4)

    print(f"[CLUSTER] {len(clusters)} trait clusters synthesized.")

if __name__ == "__main__":
    main()
