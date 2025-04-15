import json
import os
from collections import defaultdict
from datetime import datetime

EMOTIVE_LOG_PATH = "memory/emotive_signal_log.json"
PREFERRED_PATH = "memory/preferred_actions.json"
AVOIDANCE_PATH = "memory/avoidance_actions.json"

PREFERENCE_WEIGHTS = {
    "resonant_pride": 3,
    "calm_alignment": 2,
    "neutral_awareness": 1,
    "identity_conflict": -2,
    "drift_discomfort": -3
}

def load_emotive_log():
    if not os.path.exists(EMOTIVE_LOG_PATH):
        print("[PrefAvoid] No emotive log found.")
        return []

    with open(EMOTIVE_LOG_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("[PrefAvoid] Emotive log corrupted.")
            return []

def analyze_tones(entries):
    tone_scores = defaultdict(int)
    tone_counts = defaultdict(int)

    for entry in entries:
        action = entry.get("action")
        tone = entry.get("tone")
        if action and tone in PREFERENCE_WEIGHTS:
            tone_scores[action] += PREFERENCE_WEIGHTS[tone]
            tone_counts[action] += 1

    averaged = {}
    for action in tone_scores:
        avg = round(tone_scores[action] / tone_counts[action], 2)
        averaged[action] = avg

    return averaged

def separate_preferences(averaged_scores):
    preferred = []
    avoid = []

    for action, score in averaged_scores.items():
        if score >= 1:
            preferred.append({"action": action, "preference_score": score})
        elif score <= -1:
            avoid.append({"action": action, "avoidance_score": score})

    return preferred, avoid

def run_preference_avoidance_mapper():
    print("[PrefAvoid] Running Preference & Avoidance Mapping...")

    entries = load_emotive_log()
    if not entries:
        print("[PrefAvoid] No entries to process.")
        return

    scores = analyze_tones(entries)
    preferred, avoid = separate_preferences(scores)

    with open(PREFERRED_PATH, "w") as f:
        json.dump({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "preferred": preferred
        }, f, indent=4)

    with open(AVOIDANCE_PATH, "w") as f:
        json.dump({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "avoid": avoid
        }, f, indent=4)

    print(f"[PrefAvoid] Preferences saved to {PREFERRED_PATH}")
    print(f"[PrefAvoid] Avoidances saved to {AVOIDANCE_PATH}")
    print("[PrefAvoid] Preference/Avoidance mapping complete.")

if __name__ == "__main__":
    run_preference_avoidance_mapper()
