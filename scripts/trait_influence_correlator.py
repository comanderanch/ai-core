# scripts/trait_influence_correlator.py

import json
from pathlib import Path
from datetime import datetime

# Paths
TRAIT_LOG_PATH = Path("memory/trait_memory_log.json")
FEEDBACK_LOG_PATH = Path("memory/trait_feedback_log.json")
OUTPUT_PATH = Path("memory/trait_influence_log.json")

def load_json(path, fallback):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return fallback
    return fallback

def correlate_influence(trait_log, feedback_log):
    influence_map = {}

    feedback_data = feedback_log.get("feedback", {})

    for trait_id, metrics in feedback_data.items():
        bias = metrics.get("avg_bias", 0.0)
        weight = metrics.get("avg_weight", 0.0)
        drift = metrics.get("drift", 0.0)

        influence_map[trait_id] = {
            "bias": bias,
            "weight": weight,
            "drift": drift,
            "magnitude": round(abs(bias - weight), 4)
        }

    return influence_map


def main():
    print("🧭 Correlating Trait Influence...")

    trait_log = load_json(TRAIT_LOG_PATH, [])
    feedback_log = load_json(FEEDBACK_LOG_PATH, {})


    if not trait_log or not feedback_log:
        print("[INFLUENCE] Missing required data. Correlation skipped.")
        return

    influence = correlate_influence(trait_log, feedback_log)

    # Timestamped result
    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "influence": influence
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[INFLUENCE] Trait influence correlation complete. {len(influence)} trait(s) analyzed.")

if __name__ == "__main__":
    main()
