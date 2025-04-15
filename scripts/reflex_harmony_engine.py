import json
import os

PRIORITY_PATH = "memory/prioritized_actions.json"
REFLEX_LOG_PATH = "memory/reflex_feedback_log.json"
HARMONY_OUTPUT_PATH = "memory/reflex_harmony_report.json"

def load_json(path):
    if not os.path.exists(path):
        print(f"[Harmony] Missing file: {path}")
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[Harmony] Corrupted JSON in {path}")
            return []

def analyze_harmony(prioritized_actions, reflex_log):
    action_counts = {}
    for entry in reflex_log:
        action = entry["action"]
        action_counts[action] = action_counts.get(action, 0) + 1

    harmony_report = []
    for item in prioritized_actions:
        action = item["action"]
        target_score = item["resonance_score"]
        actual_count = action_counts.get(action, 0)

        # Harmony metric: how well the actual behavior matches the expected resonance
        delta = target_score - actual_count
        harmony = round(100 - (abs(delta) / target_score * 100), 2) if target_score > 0 else 0

        harmony_report.append({
            "action": action,
            "resonance_score": target_score,
            "observed_count": actual_count,
            "harmony_percent": max(0, harmony)
        })

    return sorted(harmony_report, key=lambda x: x["harmony_percent"], reverse=True)

def run_reflex_harmony_engine():
    print("[Harmony] Running Reflex Harmony Engine...")

    prioritized_actions = load_json(PRIORITY_PATH)
    reflex_log = load_json(REFLEX_LOG_PATH)

    if not prioritized_actions or not reflex_log:
        print("[Harmony] Insufficient data for harmony analysis.")
        return

    report = analyze_harmony(prioritized_actions, reflex_log)

    with open(HARMONY_OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=4)

    print(f"[Harmony] Reflex harmony report saved to {HARMONY_OUTPUT_PATH}")
    print("[Harmony] Alignment scan complete.")

if __name__ == "__main__":
    run_reflex_harmony_engine()
