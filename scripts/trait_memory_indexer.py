# scripts/trait_memory_indexer.py

import json
from pathlib import Path
from datetime import datetime

MEMORY_LOG = Path("memory/trait_memory_log.json")
INDEX_PATH = Path("memory/trait_memory_index.json")

def load_json(path, default):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def index_trait_memory():
    print("📚 Indexing Trait Memory...")

    memory_entries = load_json(MEMORY_LOG, [])
    index = {}

    for entry in memory_entries:
        trait_id = entry.get("trait_id")
        if trait_id:
            index[trait_id] = {
                "label": entry.get("label"),
                "reflex": entry.get("reflex"),
                "trait": entry.get("trait"),
                "bias": entry.get("bias"),
                "weight": entry.get("weight"),
                "timestamp": entry.get("timestamp"),
            }

    save_json(INDEX_PATH, index)

    print(f"[INDEX] {len(index)} traits indexed and saved to {INDEX_PATH.name}")

if __name__ == "__main__":
    index_trait_memory()
