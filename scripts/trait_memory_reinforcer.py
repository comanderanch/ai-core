# scripts/trait_memory_reinforcer.py

import json
from datetime import datetime
from pathlib import Path

# File paths
WEIGHT_LOG = Path("memory/reflex_weight_log.json")
BIAS_LOG = Path("memory/memory_bias_log.json")
TRAIT_LOG = Path("memory/reflex_response_log.json")
TRAIT_MEMORY_LOG = Path("memory/trait_memory_log.json")
TRAIT_INDEX = Path("memory/trait_memory_index.json")

def load_json(path, default):
    if path.exists():
        try:
            with open(path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return default
    return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def reinforce_trait():
    # Load logs
    reflex_log = load_json(TRAIT_LOG, {})
    weight_map = load_json(WEIGHT_LOG, {})
    bias_entries = load_json(BIAS_LOG, [])
    memory_log = load_json(TRAIT_MEMORY_LOG, [])
    memory_index = load_json(TRAIT_INDEX, {})

    label = reflex_log.get("label")
    reflex = reflex_log.get("reflex")
    trait = reflex_log.get("trait")
    timestamp = reflex_log.get("timestamp")

    if not (label and reflex and trait and timestamp):
        print("[TRAIT] Missing response log data. Aborting.")
        return

    # Convert list to label → bias
    bias_map = {entry["label"]: entry["bias"] for entry in bias_entries if "label" in entry and "bias" in entry}
    bias = bias_map.get(label)
    weight = weight_map.get(reflex)

    if bias is None or weight is None:
        print("[TRAIT] Missing weight or bias. Skipping.")
        return

    trait_id = f"{label}:{reflex}:{trait}"

    # Update trait memory index (for quick lookup)
    memory_index[trait_id] = {
        "bias": bias,
        "weight": weight,
        "trait": trait,
        "reflex": reflex,
        "label": label,
        "timestamp": timestamp
    }

    memory_log.append({
        "timestamp": datetime.utcnow().isoformat(),
        "trait_id": trait_id,
        "label": label,
        "reflex": reflex,
        "trait": trait,
        "bias": bias,
        "weight": weight
    })

    save_json(TRAIT_MEMORY_LOG, memory_log)
    save_json(TRAIT_INDEX, memory_index)

    print(f"[TRAIT] Memory reinforced: {trait_id}")

if __name__ == "__main__":
    print("🧠 Reinforcing Trait Memory...")
    reinforce_trait()
