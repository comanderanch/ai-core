# scripts/trait_relationship_mapper.py

import json
from pathlib import Path
from collections import defaultdict

# Paths
TRAIT_LOG_PATH = Path("memory/trait_memory_log.json")
RELATIONSHIP_MAP_PATH = Path("memory/trait_relationship_map.json")

def load_json(path, default):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def generate_relationship_graph(entries):
    graph = defaultdict(lambda: {"labels": set(), "reflexes": set()})

    for entry in entries:
        trait = entry["trait"]
        label = entry["label"]
        reflex = entry["reflex"]

        graph[trait]["labels"].add(label)
        graph[trait]["reflexes"].add(reflex)

    # Convert sets to sorted lists for JSON compatibility
    return {
        trait: {
            "labels": sorted(list(data["labels"])),
            "reflexes": sorted(list(data["reflexes"]))
        }
        for trait, data in graph.items()
    }

def main():
    print("🧭 Generating Trait Relationship Map...")

    entries = load_json(TRAIT_LOG_PATH, [])
    if not entries:
        print("[WARN] No entries found in trait_memory_log.json")
        return

    relationship_map = generate_relationship_graph(entries)
    save_json(RELATIONSHIP_MAP_PATH, relationship_map)

    print(f"[MAP] {len(relationship_map)} trait relationships mapped and saved.")

if __name__ == "__main__":
    main()
