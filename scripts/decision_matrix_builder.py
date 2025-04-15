import json
import os
from datetime import datetime

RECALL_LOG_PATH = "memory/contextual_recall_log.json"
DECISION_MATRIX_PATH = "memory/decision_matrix.json"

def load_json(path):
    if not os.path.exists(path):
        print(f"[DecisionMatrix] Missing file: {path}")
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[DecisionMatrix] Corrupted JSON in {path}")
            return []

def build_decision_matrix(recall_data):
    decision_matrix = []
    for item in recall_data:
        score = (
            item["matched_tokens"] * 2 +     # Context match is high priority
            item["resonance_weight"] * 1 +   # Past behavioral frequency
            item["harmony_average"] * 0.5    # Historical alignment
        )
        decision_matrix.append({
            "concept": item["concept"],
            "decision_score": round(score, 2),
            "context_tokens": item["linked_tokens"],
            "resonance_weight": item["resonance_weight"],
            "harmony_average": item["harmony_average"],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    return sorted(decision_matrix, key=lambda x: x["decision_score"], reverse=True)

def run_decision_matrix_builder():
    print("[DecisionMatrix] Generating Decision Matrix...")

    recall_data = load_json(RECALL_LOG_PATH)
    if not recall_data:
        print("[DecisionMatrix] No recall data available.")
        return

    matrix = build_decision_matrix(recall_data)

    with open(DECISION_MATRIX_PATH, "w") as f:
        json.dump(matrix, f, indent=4)

    print(f"[DecisionMatrix] Decision matrix saved to {DECISION_MATRIX_PATH}")
    print("[DecisionMatrix] Prioritization complete.")

if __name__ == "__main__":
    run_decision_matrix_builder()
