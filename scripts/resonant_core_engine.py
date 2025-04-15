import json
import os
from collections import defaultdict

REFLEX_LOG_PATH = "memory/reflex_feedback_log.json"
ANCHOR_PATH = "memory/core_anchors.json"
OUTPUT_PATH = "memory/resonant_token_map.json"

def load_json(path):
    if not os.path.exists(path):
        print(f"[ResonantCore] Missing file: {path}")
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[ResonantCore] Corrupted JSON in {path}")
            return []

def build_resonance_map(reflex_log, anchor_data):
    resonance = defaultdict(lambda: {"count": 0, "identity_weight": 0})

    # Count base reflex frequency
    for entry in reflex_log:
        action = entry["action"]
        resonance[action]["count"] += 1

    # Add identity weight from anchor patterns
    for anchor in anchor_data:
        for action in anchor.get("based_on", []):
            resonance[action]["identity_weight"] += 1

    # Build scored output
    final_map = []
    for action, data in resonance.items():
        final_map.append({
            "action": action,
            "count": data["count"],
            "identity_weight": data["identity_weight"],
            "resonance_score": round((data["count"] + data["identity_weight"] * 2), 2)
        })

    return sorted(final_map, key=lambda x: x["resonance_score"], reverse=True)

def run_resonant_core_engine():
    print("[ResonantCore] Activating Resonant Core Engine...")

    reflex_log = load_json(REFLEX_LOG_PATH)
    anchor_data = load_json(ANCHOR_PATH)

    if not reflex_log:
        print("[ResonantCore] No reflex feedback found.")
        return

    resonance_map = build_resonance_map(reflex_log, anchor_data)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(resonance_map, f, indent=4)

    print(f"[ResonantCore] Resonant map saved to {OUTPUT_PATH}")
    print("[ResonantCore] Core resonance complete.")

if __name__ == "__main__":
    run_resonant_core_engine()
