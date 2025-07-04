# scripts/trait_equilibrium_tracker.py

import json
from pathlib import Path
from datetime import datetime

MASTER_LOG_PATH = Path("memory/trait_master_log.json")
OUTPUT_LOG_PATH = Path("memory/trait_equilibrium_log.json")

def load_json(path, fallback):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return fallback
    return fallback

def calculate_equilibrium(master_log):
    traits = master_log.get("unified_traits", {})
    total = len(traits)

    if total == 0:
        return {
            "total_traits": 0,
            "avg_bias": 0.0,
            "avg_weight": 0.0,
            "avg_drift": 0.0,
            "imbalance_score": 0.0
        }

    bias_sum = 0.0
    weight_sum = 0.0
    drift_sum = 0.0
    imbalance = 0.0

    for trait_id, data in traits.items():
        bias = data.get("bias", 0.0)
        weight = data.get("weight", 0.0)
        drift = abs(weight - bias)

        bias_sum += bias
        weight_sum += weight
        drift_sum += drift
        imbalance += abs(bias - weight)

    avg_bias = round(bias_sum / total, 4)
    avg_weight = round(weight_sum / total, 4)
    avg_drift = round(drift_sum / total, 4)
    imbalance_score = round(imbalance / total, 4)

    return {
        "total_traits": total,
        "avg_bias": avg_bias,
        "avg_weight": avg_weight,
        "avg_drift": avg_drift,
        "imbalance_score": imbalance_score
    }

def main():
    print("🧮 Tracking Trait Equilibrium...")

    master_log = load_json(MASTER_LOG_PATH, {})
    summary = calculate_equilibrium(master_log)

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "summary": summary
    }

    with open(OUTPUT_LOG_PATH, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[EQUILIBRIUM] Summary recorded for {summary['total_traits']} traits.")

if __name__ == "__main__":
    main()
