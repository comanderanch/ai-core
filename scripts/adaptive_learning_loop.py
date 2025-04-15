import json
import os
from collections import defaultdict
from datetime import datetime

DECISION_MATRIX_PATH = "memory/decision_matrix.json"
FEEDBACK_LOG_PATH = "memory/reflex_feedback_log.json"
OUTPUT_PATH = "memory/adaptive_learning_update.json"

def load_json(path):
    if not os.path.exists(path):
        print(f"[Adaptive] Missing file: {path}")
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[Adaptive] Corrupted JSON in {path}")
            return []

def analyze_feedback(feedback_log):
    counter = defaultdict(int)
    for entry in feedback_log:
        action = entry.get("action")
        if action:
            counter[action] += 1
    return counter

def generate_learning_update(decision_matrix, feedback_counter):
    learning_update = []
    for entry in decision_matrix:
        action = entry["concept"]
        prior_score = entry["decision_score"]
        reflex_count = feedback_counter.get(action, 0)

        # Learn: if an action is used more often, raise its score
        adjusted_score = round(prior_score + (reflex_count * 0.5), 2)

        learning_update.append({
            "concept": action,
            "original_score": prior_score,
            "reflex_count": reflex_count,
            "adjusted_score": adjusted_score,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    return learning_update

def run_adaptive_learning_loop():
    print("[Adaptive] Starting Adaptive Learning Loop...")

    matrix = load_json(DECISION_MATRIX_PATH)
    feedback = load_json(FEEDBACK_LOG_PATH)

    if not matrix or not feedback:
        print("[Adaptive] Missing matrix or feedback data.")
        return

    feedback_counter = analyze_feedback(feedback)
    learning_update = generate_learning_update(matrix, feedback_counter)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(learning_update, f, indent=4)

    print(f"[Adaptive] Learning update saved to {OUTPUT_PATH}")
    print("[Adaptive] Behavior adjustment calculation complete.")

if __name__ == "__main__":
    run_adaptive_learning_loop()
