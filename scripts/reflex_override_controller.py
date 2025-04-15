import json
import os
from datetime import datetime

REFLEX_TOKENS = [20, 40]  # Example triggered tokens
REFLEX_ACTIONS = {
    20: "Trigger Action A",
    40: "Trigger Action B"
}

PREFERRED_PATH = "memory/preferred_actions.json"
AVOID_PATH = "memory/avoidance_actions.json"
ANCHOR_PATH = "memory/core_anchors.json"

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[Override] Failed to load {path}")
            return []

def is_preferred(action, preferred):
    return any(p["action"] == action for p in preferred)

def is_avoided(action, avoid):
    return any(a["action"] == action for a in avoid)

def is_identity_aligned(action, anchors):
    for anchor in anchors:
        if action in anchor.get("linked_tokens", []):
            return True
    return False

def run_override_controller():
    print("[Override] Initiating Reflex Override System...")

    preferred = load_json(PREFERRED_PATH).get("preferred", [])
    avoid = load_json(AVOID_PATH).get("avoid", [])
    anchors = load_json(ANCHOR_PATH)

    final_actions = []

    for token in REFLEX_TOKENS:
        action = REFLEX_ACTIONS.get(token)
        if not action:
            continue

        print(f"\n[Override] Evaluating: {action}")

        if is_avoided(action, avoid):
            print(f"[Override] ❌ Skipped — Action is marked for avoidance.")
            continue

        if not is_identity_aligned(action, anchors):
            print(f"[Override] ⚠️ Skipped — Not aligned with core anchors.")
            continue

        if is_preferred(action, preferred):
            print(f"[Override] ✅ Allowed — Action preferred and aligned.")
            final_actions.append(action)
        else:
            print(f"[Override] ⏸️ Allowed with caution — No conflict detected.")

    print("\n[Override] Final approved actions:", final_actions)
    print("[Override] Reflex filtering complete.")

if __name__ == "__main__":
    run_override_controller()
