# scripts/trait_feedback_analyzer.py

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

TRAIT_LOG_PATH = Path("memory/trait_memory_log.json")
OUTPUT_LOG_PATH = Path("memory/trait_feedback_log.json")

def load_json(path, default):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return default

def analyze_feedback(log_entries):
    trait_summary = defaultdict(lambda: {"count": 0, "bias_total": 0.0, "weight_total": 0.0})

    for entry in log_entries:
        trait_id = entry.get("trait_id")
        if not trait_id:
            continue
        trait_summary[trait_id]["count"] += 1
        trait_summary[trait_id]["bias_total"] += entry.get("bias", 0.0)
        trait_summary[trait_id]["weight_total"] += entry.get("weight", 0.0)

    results = {}
    for trait_id, values in trait_summary.items():
        count = values["count"]
        avg_bias = round(values["bias_total"] / count, 3)
        avg_weight = round(values["weight_total"] / count, 3)
        drift = round(abs(avg_bias - avg_weight), 3)

        results[trait_id] = {
            "entries": count,
            "avg_bias": avg_bias,
            "avg_weight": avg_weight,
            "drift": drift
        }

    return results

def save_feedback(feedback_data):
    with open(OUTPUT_LOG_PATH, "w") as f:
        json.dump({
            "timestamp": datetime.utcnow().isoformat(),
            "feedback": feedback_data
        }, f, indent=4)

def main():
    print("📈 Analyzing Trait Feedback...")
    trait_log = load_json(TRAIT_LOG_PATH, [])
    feedback_data = analyze_feedback(trait_log)
    save_feedback(feedback_data)
    print(f"[FEEDBACK] {len(feedback_data)} trait(s) analyzed and saved.")

if __name__ == "__main__":
    main()
