import json
import os

RESONANT_MAP_PATH = "memory/resonant_token_map.json"
FILTERED_OUTPUT_PATH = "memory/prioritized_actions.json"

# Minimum score to consider an action meaningful
RESONANCE_THRESHOLD = 10

def load_json(path):
    if not os.path.exists(path):
        print(f"[ResonantFilter] Missing file: {path}")
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[ResonantFilter] Corrupted JSON in {path}")
            return []

def filter_high_resonance_actions(resonant_map, threshold):
    prioritized = []
    for item in resonant_map:
        if item["resonance_score"] >= threshold:
            prioritized.append({
                "action": item["action"],
                "resonance_score": item["resonance_score"]
            })
    return prioritized

def run_resonant_behavior_filter():
    print("[ResonantFilter] Analyzing resonance map for priority actions...")

    resonant_map = load_json(RESONANT_MAP_PATH)
    if not resonant_map:
        print("[ResonantFilter] No resonance data found.")
        return

    prioritized_actions = filter_high_resonance_actions(resonant_map, RESONANCE_THRESHOLD)

    with open(FILTERED_OUTPUT_PATH, "w") as f:
        json.dump(prioritized_actions, f, indent=4)

    if prioritized_actions:
        print(f"[ResonantFilter] {len(prioritized_actions)} high-priority actions saved to {FILTERED_OUTPUT_PATH}")
    else:
        print("[ResonantFilter] No actions passed the resonance threshold.")

if __name__ == "__main__":
    run_resonant_behavior_filter()
