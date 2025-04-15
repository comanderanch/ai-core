import json
import os

ECHO_MAP_PATH = "memory/cognitive_echo_map.json"
ANCHOR_PATH = "memory/core_anchors.json"

# Frequency threshold — how many repeats to qualify as an anchor
ANCHOR_THRESHOLD = 3

def load_echo_map():
    if not os.path.exists(ECHO_MAP_PATH):
        print("[Anchor Gen] Echo map not found.")
        return []

    with open(ECHO_MAP_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("[Anchor Gen] Invalid echo map.")
            return []

def generate_anchors(echo_patterns):
    anchors = []
    for pattern in echo_patterns:
        count = pattern.get("count", 0)
        actions = pattern.get("pattern", [])

        if count >= ANCHOR_THRESHOLD:
            anchor_label = identify_anchor_type(actions)
            anchors.append({
                "anchor": anchor_label,
                "based_on": actions,
                "count": count
            })

    return anchors

def identify_anchor_type(actions):
    if all(action == "Trigger Action A" for action in actions):
        return "Persistent Reinforcement"
    elif all(action == "Trigger Action B" for action in actions):
        return "Adaptive Redirection"
    else:
        return "Mixed Reflex Identity"

def save_anchors(anchors):
    with open(ANCHOR_PATH, "w") as f:
        json.dump(anchors, f, indent=4)
    print(f"[Anchor Gen] Anchors saved to {ANCHOR_PATH}")

def run_anchor_generator():
    print("[Anchor Gen] Generating core identity anchors...")
    echo_patterns = load_echo_map()
    anchors = generate_anchors(echo_patterns)
    save_anchors(anchors)
    print("[Anchor Gen] Anchor generation complete.")

if __name__ == "__main__":
    run_anchor_generator()
