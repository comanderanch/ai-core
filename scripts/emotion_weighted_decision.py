import json
import os
from datetime import datetime
from collections import defaultdict

DECISION_MATRIX_PATH = "memory/decision_matrix.json"
EMOTIVE_LOG_PATH = "memory/emotive_signal_log.json"
OUTPUT_PATH = "memory/emotionally_weighted_decisions.json"

# Tone weightings – how much each feeling should influence decision weight
TONE_WEIGHTS = {
    "resonant_pride": 1.0,
    "calm_alignment": 0.75,
    "neutral_awareness": 0.5,
    "identity_conflict": -0.5,
    "drift_discomfort": -1.0
}

def load_json(path):
    if not os.path.exists(path):
        print(f"[EmotionWeighting] Missing file: {path}")
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[EmotionWeighting] Corrupted JSON in {path}")
            return []

def aggregate_emotive_scores(log):
    score_map = defaultdict(list)
    for entry in log:
        tone = entry.get("tone")
        action = entry.get("action")
        if tone and action:
            score_map[action].append(TONE_WEIGHTS.get(tone, 0))
    # Average each action’s emotional weight
    final = {}
    for action, scores in score_map.items():
        avg = round(sum(scores) / len(scores), 3)
        final[action] = avg
    return final

def build_emotionally_weighted_matrix(decision_matrix, emotive_scores):
    enhanced = []
    for entry in decision_matrix:
        action = entry["concept"]
        base_score = entry["decision_score"]
        tone_weight = emotive_scores.get(action, 0)

        adjusted = round(base_score + (tone_weight * 5), 2)

        enhanced.append({
            "concept": action,
            "base_score": base_score,
            "tone_weight": tone_weight,
            "adjusted_score": adjusted,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    return enhanced

def run_emotion_weighting():
    print("[EmotionWeighting] Enhancing decision matrix with emotional tone...")

    decision_matrix = load_json(DECISION_MATRIX_PATH)
    emotive_log = load_json(EMOTIVE_LOG_PATH)

    if not decision_matrix or not emotive_log:
        print("[EmotionWeighting] Missing required memory components.")
        return

    emotive_scores = aggregate_emotive_scores(emotive_log)
    enhanced_matrix = build_emotionally_weighted_matrix(decision_matrix, emotive_scores)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(enhanced_matrix, f, indent=4)

    print(f"[EmotionWeighting] Enhanced decisions saved to {OUTPUT_PATH}")
    print("[EmotionWeighting] Emotional cognition complete.")

if __name__ == "__main__":
    run_emotion_weighting()
