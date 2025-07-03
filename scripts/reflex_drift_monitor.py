# scripts/reflex_drift_monitor.py

import json
from pathlib import Path
from datetime import datetime

WEIGHT_LOG = Path("memory/reflex_weight_log.json")
REINFORCEMENT_LOG = Path("memory/reflex_reinforcement_log.json")
DECAY_LOG = Path("memory/reflex_decay_log.json")
DRIFT_LOG = Path("memory/reflex_drift_log.json")

def load_json(path, default):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return default

def detect_drift():
    weights = load_json(WEIGHT_LOG, {})
    reinforcements = load_json(REINFORCEMENT_LOG, [])
    decays = load_json(DECAY_LOG, [])

    drift_report = []

    for reflex in weights:
        reinforcement_total = sum(
            r["new_weight"] - r["original_weight"]
            for entry in reinforcements
            for r in entry["reinforced"]
            if r["reflex"] == reflex
        )

        decay_total = sum(
            d["old_weight"] - d["new_weight"]
            for d in decays
            if d["reflex"] == reflex
        )

        net_change = reinforcement_total - decay_total

        drift_report.append({
            "timestamp": datetime.utcnow().isoformat(),
            "reflex": reflex,
            "reinforcement_gain": round(reinforcement_total, 3),
            "decay_loss": round(decay_total, 3),
            "net_change": round(net_change, 3),
            "status": (
                "positive drift" if net_change > 0.05 else
                "negative drift" if net_change < -0.05 else
                "stable"
            )
        })

    with open(DRIFT_LOG, "w") as f:
        json.dump(drift_report, f, indent=4)

    print("[DRIFT] Drift analysis complete.")

if __name__ == "__main__":
    print("📡 Monitoring reflex drift...")
    detect_drift()
