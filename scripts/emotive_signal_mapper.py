import json
import os
from datetime import datetime

FEEDBACK_PATH = "memory/reflex_feedback_log.json"
HARMONY_PATH = "memory/harmony_tuning_report.json"
ANCHOR_PATH = "memory/core_anchors.json"
OUTPUT_PATH = "memory/emotive_signal_log.json"

def load_json(path):
    if not os.path.exists(path):
        print(f"[EmotiveMap] Missing file: {path}")
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[EmotiveMap] Corrupted JSON in {path}")
            return []

def determine_emotive_tone(action, harmony_map, anchors):
    harmony_score = 0
    for entry in harmony_map:
        if entry["action"] == action:
            harmony_score = entry["harmony_percent"]
            break

    identity_weight = 0
    for anchor in anchors:
        if action in anchor.get("linked_tokens", []):
            identity_weight = anchor.get("resonance_weight", 0)
            break

    # Assign tone based on harmony + identity strength
    if harmony_score >= 70 and identity_weight >= 10:
        return "resonant_pride"
    elif harmony_score >= 50:
        return "calm_alignment"
    elif 30 <= harmony_score < 50:
        return "neutral_awareness"
    elif identity_weight > 5:
        return "identity_conflict"
    else:
        return "drift_discomfort"

def run_emotive_signal_mapper():
    print("[EmotiveMap] Running Emotive Signal Mapping...")

    feedback = load_json(FEEDBACK_PATH)
    harmony_report = load_json(HARMONY_PATH).get("analysis", [])
    anchors = load_json(ANCHOR_PATH)

    if not feedback:
        print("[EmotiveMap] No feedback log found.")
        return

    tone_log = []
    for entry in feedback:
        action = entry.get("action")
        if not action:
            continue

        tone = determine_emotive_tone(action, harmony_report, anchors)
        tone_log.append({
            "action": action,
            "tone": tone,
            "timestamp": entry.get("timestamp", datetime.utcnow().isoformat() + "Z")
        })

    with open(OUTPUT_PATH, "w") as f:
        json.dump(tone_log, f, indent=4)

    print(f"[EmotiveMap] Emotive signal log saved to {OUTPUT_PATH}")
    print("[EmotiveMap] Emotional tone mapping complete.")

if __name__ == "__main__":
    run_emotive_signal_mapper()
