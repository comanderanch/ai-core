import json
import os
from datetime import datetime

FEEDBACK_LOG_PATH = "memory/reflex_feedback_log.json"
HARMONY_REPORT_PATH = "memory/reflex_harmony_report.json"
OUTPUT_PATH = "memory/harmony_tuning_report.json"

def load_json(path):
    if not os.path.exists(path):
        print(f"[HarmonyTuner] Missing file: {path}")
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[HarmonyTuner] Corrupted JSON in {path}")
            return []

def count_reflex_frequency(feedback_log):
    frequency = {}
    for entry in feedback_log:
        action = entry.get("action")
        if action:
            frequency[action] = frequency.get(action, 0) + 1
    return frequency

def load_harmony_scores(harmony_report):
    scores = {}
    for entry in harmony_report:
        action = entry.get("action")
        score = entry.get("harmony_percent", 0)
        if action:
            scores[action] = score
    return scores

def analyze_alignment(frequencies, harmony_scores):
    report = []
    for action, freq in frequencies.items():
        harmony = harmony_scores.get(action, 0)
        imbalance = round(freq * (1 - (harmony / 100)), 2)

        report.append({
            "action": action,
            "reflex_count": freq,
            "harmony_percent": harmony,
            "imbalance_score": imbalance
        })

    return sorted(report, key=lambda x: x["imbalance_score"], reverse=True)

def run_harmony_tuner():
    print("[HarmonyTuner] Running Reflex Harmony Tuner...")

    feedback_log = load_json(FEEDBACK_LOG_PATH)
    harmony_report = load_json(HARMONY_REPORT_PATH)

    if not feedback_log or not harmony_report:
        print("[HarmonyTuner] Required logs not found or incomplete.")
        return

    frequencies = count_reflex_frequency(feedback_log)
    harmony_scores = load_harmony_scores(harmony_report)
    alignment = analyze_alignment(frequencies, harmony_scores)

    output = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "analysis": alignment
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=4)

    print(f"[HarmonyTuner] Harmony tuning report saved to {OUTPUT_PATH}")
    print("[HarmonyTuner] Reflex alignment analysis complete.")

if __name__ == "__main__":
    run_harmony_tuner()
