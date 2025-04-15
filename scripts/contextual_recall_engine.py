import json
import os
from datetime import datetime

EXPANDED_MAP_PATH = "memory/expanded_memory_map.json"
CONTEXTUAL_RECALL_OUTPUT = "memory/contextual_recall_log.json"

# Tokens we're simulating as "current context"
SIMULATED_CONTEXT = ["Trigger Action A"]  # You can expand this list as new tokens emerge

def load_json(path):
    if not os.path.exists(path):
        print(f"[Recall] Missing file: {path}")
        return {}
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[Recall] Corrupted JSON in {path}")
            return {}

def recall_relevant_concepts(memory_map, context_tokens):
    results = []
    for concept, data in memory_map.items():
        match_count = sum(1 for t in context_tokens if t in data["linked_tokens"])
        if match_count > 0:
            results.append({
                "concept": concept,
                "matched_tokens": match_count,
                "linked_tokens": data["linked_tokens"],
                "resonance_weight": data["resonance_weight"],
                "harmony_average": data["harmony_average"],
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
    return sorted(results, key=lambda x: (x["matched_tokens"], x["resonance_weight"]), reverse=True)

def run_contextual_recall():
    print("[Recall] Running Contextual Recall Engine...")

    memory_map = load_json(EXPANDED_MAP_PATH)
    if not memory_map:
        print("[Recall] Memory map not found or empty.")
        return

    recall_results = recall_relevant_concepts(memory_map, SIMULATED_CONTEXT)

    with open(CONTEXTUAL_RECALL_OUTPUT, "w") as f:
        json.dump(recall_results, f, indent=4)

    if recall_results:
        print(f"[Recall] Recall results saved to {CONTEXTUAL_RECALL_OUTPUT}")
        for r in recall_results:
            print(f"[Recall] => {r['concept']} (matched {r['matched_tokens']} tokens)")
    else:
        print("[Recall] No relevant concepts found for current context.")

if __name__ == "__main__":
    run_contextual_recall()
