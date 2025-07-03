# scripts/reflex_stability_evaluator.py

import json
from pathlib import Path
from datetime import datetime

WEIGHT_LOG = Path("memory/reflex_weight_log.json")
REINFORCE_LOG = Path("memory/reflex_reinforcement_log.json")
DECAY_LOG = Path("memory/reflex_decay_log.json")
SCORE_LOG = Path("memory/reflex_response_score.json")
OUTPUT_LOG = Path("memory/reflex_stability_report.json")

def load_json(path):
    if not path.exists():
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def main():
    print("📊 Evaluating Reflex Stability...")

    weight_map = load_json(WEIGHT_LOG)
    reinforcement_data = load_json(REINFORCE_LOG)
    decay_data = load_json(DECAY_LOG)
    score_data = load_json(SCORE_LOG)

    stability_report = {}

    # Build reinforcement count
    reinforce_counts = {}
    if isinstance(reinforcement_data, list):
        for entry in reinforcement_data:
            for r in entry.get("reinforced", []):
                reflex = r["reflex"]
                reinforce_counts[reflex] = reinforce_counts.get(reflex, 0) + 1

    # Build decay count
    decay_counts = {}
    if isinstance(decay_data, list):
        for entry in decay_data:
            reflex = entry.get("reflex")
            decay_counts[reflex] = decay_counts.get(reflex, 0) + 1

    # Score summary
    if score_data and isinstance(score_data, dict):
        reflex = score_data.get("reflex")
        score = score_data.get("score")
        if reflex:
            stability_report[reflex] = {
                "weight": weight_map.get(reflex),
                "reinforced": reinforce_counts.get(reflex, 0),
                "decayed": decay_counts.get(reflex, 0),
                "score": score,
                "status": "stable" if reinforce_counts.get(reflex, 0) >= decay_counts.get(reflex, 0) else "drifting",
                "timestamp": datetime.utcnow().isoformat()
            }

    with open(OUTPUT_LOG, "w") as f:
        json.dump(stability_report, f, indent=4)

    print("✅ Stability analysis complete.")

if __name__ == "__main__":
    main()
