import json
import os
from collections import defaultdict, Counter

REFLEX_LOG_PATH = "memory/reflex_feedback_log.json"
ANCHOR_PATH = "memory/core_anchors.json"
HARMONY_PATH = "memory/reflex_harmony_report.json"
OUTPUT_PATH = "memory/expanded_memory_map.json"

def load_json(path):
    if not os.path.exists(path):
        print(f"[MemoryMap] Missing file: {path}")
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[MemoryMap] Corrupted JSON in {path}")
            return []

def build_token_concepts(reflex_log, anchor_data, harmony_data):
    concept_map = defaultdict(lambda: {
        "linked_tokens": set(),
        "resonance_weight": 0,
        "anchor_count": 0,
        "harmony_average": 0.0
    })

    harmony_lookup = {entry["action"]: entry["harmony_percent"] for entry in harmony_data}

    for anchor in anchor_data:
        base = anchor["anchor"]
        linked = anchor.get("based_on", [])

        for token in linked:
            concept_map[base]["linked_tokens"].add(token)
            concept_map[base]["anchor_count"] += 1
            concept_map[base]["resonance_weight"] += 1
            concept_map[base]["harmony_average"] += harmony_lookup.get(token, 0)

    # Token reflex log scoring
    token_counts = Counter(entry["action"] for entry in reflex_log)

    for concept, data in concept_map.items():
        for token in data["linked_tokens"]:
            data["resonance_weight"] += token_counts.get(token, 0)

        if data["anchor_count"] > 0:
            data["harmony_average"] = round(data["harmony_average"] / data["anchor_count"], 2)

        data["linked_tokens"] = list(data["linked_tokens"])

    return concept_map

def run_memory_expansion_mapper():
    print("[MemoryMap] Running Memory Expansion Mapping...")

    reflex_log = load_json(REFLEX_LOG_PATH)
    anchors = load_json(ANCHOR_PATH)
    harmony = load_json(HARMONY_PATH)

    if not reflex_log or not anchors or not harmony:
        print("[MemoryMap] Insufficient data for mapping.")
        return

    memory_concepts = build_token_concepts(reflex_log, anchors, harmony)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(memory_concepts, f, indent=4)

    print(f"[MemoryMap] Memory map saved to {OUTPUT_PATH}")
    print("[MemoryMap] Concept memory expansion complete.")

if __name__ == "__main__":
    run_memory_expansion_mapper()
