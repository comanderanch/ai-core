# scripts/reflex_adaptation_engine.py

import json
from datetime import datetime
from pathlib import Path

# File paths
RESPONSE_SCORE_PATH = Path("memory/reflex_response_score.json")
REINFORCEMENT_LOG_PATH = Path("memory/reflex_reinforcement_log.json")
DECAY_LOG_PATH = Path("memory/reflex_decay_log.json")
OUTPUT_LOG_PATH = Path("memory/reflex_adaptation_log.json")

def load_json(path):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def main():
    print("⚙️  Running Reflex Adaptation Engine...")

    response_data = load_json(RESPONSE_SCORE_PATH)
    reinforcement_log = load_json(REINFORCEMENT_LOG_PATH)
    decay_log = load_json(DECAY_LOG_PATH)

    if not response_data or not reinforcement_log or not decay_log:
        print("[ADAPT] Missing required input logs. Adaptation skipped.")
        return

    reflex = response_data.get("reflex")
    label = response_data.get("label")
    trait = response_data.get("trait")
    score = response_data.get("score")

    # Find latest reinforcement
    reinforcement = next(
        (item for log in reversed(reinforcement_log)
         for item in log.get("reinforced", [])
         if item.get("reflex") == reflex),
        None
    )

    # Find latest decay
    decay = next(
        (item for item in reversed(decay_log)
         if item.get("reflex") == reflex),
        None
    )

    if not reinforcement or not decay:
        print(f"[ADAPT] Incomplete data for reflex '{reflex}'. Skipping.")
        return

    original_weight = reinforcement["original_weight"]
    reinforced_weight = reinforcement["new_weight"]
    decayed_weight = decay["new_weight"]

    adaptation_trend = "stable"
    if score >= 0.9 and reinforced_weight > original_weight:
        adaptation_trend = "positive"
    elif score <= 0.5 and decayed_weight < original_weight:
        adaptation_trend = "negative"

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "reflex": reflex,
        "label": label,
        "trait": trait,
        "original_weight": original_weight,
        "reinforced_weight": reinforced_weight,
        "decayed_weight": decayed_weight,
        "score": score,
        "trend": adaptation_trend
    }

    # Append to adaptation log
    if OUTPUT_LOG_PATH.exists():
        try:
            with open(OUTPUT_LOG_PATH, "r") as f:
                content = f.read().strip()
                data = json.loads(content) if content else []
        except Exception as e:
            print(f"[WARN] Failed to load existing adaptation log: {e}")
            data = []
    else:
        data = []


    data.append(result)

    with open(OUTPUT_LOG_PATH, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[ADAPT] Reflex '{reflex}' trend recorded as: {adaptation_trend}")

if __name__ == "__main__":
    main()
