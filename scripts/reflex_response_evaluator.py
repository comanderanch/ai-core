# scripts/reflex_response_evaluator.py

import json
from datetime import datetime
from pathlib import Path

# Paths
RESPONSE_LOG = Path("memory/reflex_response_log.json")
WEIGHT_LOG = Path("memory/reflex_weight_log.json")
BIAS_LOG = Path("memory/memory_bias_log.json")
SCORE_LOG = Path("memory/reflex_response_score.json")

def load_json(path):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def evaluate_reflex(reflex_name, bias, weight):
    """
    Evaluation Scoring Logic:
    - Score ranges from 0.0 to 1.0
    - Perfect alignment (bias ≈ weight): score = 1.0
    - Large deviation: lower score
    """
    score = 1.0 - abs(bias - weight)
    return round(max(0.0, min(1.0, score)), 3)

def main():
    print("🟢 START: Reflex Evaluator engaged")

   # print("[DEBUG] Starting evaluation...")

    # Load logs
    reflex_log = load_json(RESPONSE_LOG)
    weight_map = load_json(WEIGHT_LOG)
    bias_log = load_json(BIAS_LOG)

   # print(f"[DEBUG] reflex_log: {reflex_log}")
   # print(f"[DEBUG] weight_map: {weight_map}")
   # print(f"[DEBUG] bias_log: {bias_log}")

    reflex_name = reflex_log.get("reflex")
    label = reflex_log.get("label")
    trait = reflex_log.get("trait")
    timestamp = reflex_log.get("timestamp")

    # Convert list to lookup dict: label → bias
    bias_map = {entry["label"]: entry["bias"] for entry in bias_log if "label" in entry and "bias" in entry}

    # 🔍 Debug prints
   # print(f"[DEBUG] Reflex: {reflex_name}, Label: {label}, Trait: {trait}")
   # print(f"[DEBUG] Weight keys: {list(weight_map.keys())}")
   # print(f"[DEBUG] Bias keys: {list(bias_map.keys())}")

    if not reflex_name or reflex_name not in weight_map or label not in bias_map:
        print("[EVAL] Missing required data. Evaluation skipped.")
        return

    weight = weight_map[reflex_name]
    bias = bias_map[label]

    score = evaluate_reflex(reflex_name, bias, weight)

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "label": label,
        "reflex": reflex_name,
        "trait": trait,
        "bias": bias,
        "weight": weight,
        "score": score
    }

    with open(SCORE_LOG, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[EVAL] Reflex '{reflex_name}' scored {score} (bias={bias}, weight={weight})")

if __name__ == "__main__":
    main()
