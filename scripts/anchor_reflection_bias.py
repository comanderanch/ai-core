import json
import os
from collections import defaultdict
from datetime import datetime

ANCHOR_PATH = "memory/core_anchors.json"
FEEDBACK_PATH = "memory/reflex_feedback_log.json"
ALIGNMENT_REPORT_PATH = "memory/anchor_alignment_report.json"

# How far back in behavior to reflect on
REFLECTION_WINDOW = 10

def load_json_file(path):
    if not os.path.exists(path):
        print(f"[Reflection] File not found: {path}")
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[Reflection] Invalid JSON in: {path}")
            return []

def get_recent_actions(feedback, limit=REFLECTION_WINDOW):
    return [entry["action"] for entry in feedback][-limit:]

def build_anchor_patterns(anchor_data):
    return [anchor["based_on"] for anchor in anchor_data]

def calculate_alignment(recent_actions, anchor_patterns):
    score = 0
    matches = []

    for pattern in anchor_patterns:
        pattern_len = len(pattern)
        for i in range(len(recent_actions) - pattern_len + 1):
            window = recent_actions[i:i+pattern_len]
            if window == pattern:
                score += 1
                matches.append(window)

    return score, matches

def run_anchor_alignment():
    print("[Reflection] Running Anchor Reflection Bias Analysis...")

    anchors = load_json_file(ANCHOR_PATH)
    feedback = load_json_file(FEEDBACK_PATH)
    recent_actions = get_recent_actions(feedback)

    anchor_patterns = build_anchor_patterns(anchors)
    score, matched_patterns = calculate_alignment(recent_actions, anchor_patterns)

    result = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "recent_actions": recent_actions,
        "anchor_alignment_score": score,
        "matched_patterns": matched_patterns
    }

    with open(ALIGNMENT_REPORT_PATH, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[Reflection] Alignment report saved to {ALIGNMENT_REPORT_PATH}")
    print(f"[Reflection] Score: {score} / {len(recent_actions)} actions")

if __name__ == "__main__":
    run_anchor_alignment()
