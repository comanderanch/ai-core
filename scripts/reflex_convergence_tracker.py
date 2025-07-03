# scripts/reflex_convergence_tracker.py

import json
from pathlib import Path
from statistics import stdev, mean
from datetime import datetime

# File paths
SYNC_LOG_PATH = Path("memory/reflex_weight_sync_log.json")
OUTPUT_PATH = Path("memory/reflex_convergence_log.json")

def load_json(path):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return []

def analyze_convergence(sync_snapshots):
    """Analyze weight patterns for convergence per reflex."""
    reflex_history = {}

    # Build historical timeline per reflex
    for snapshot in sync_snapshots:
        weights = snapshot.get("weights", {})
        for reflex, weight in weights.items():
            reflex_history.setdefault(reflex, []).append(weight)

    results = []
    for reflex, weight_list in reflex_history.items():
        if len(weight_list) < 2:
            trend = "insufficient data"
            variability = 0.0
        else:
            variability = round(stdev(weight_list), 4)
            avg_weight = round(mean(weight_list), 4)

            if variability < 0.05:
                trend = "converging"
            elif variability < 0.15:
                trend = "oscillating"
            else:
                trend = "diverging"

        results.append({
            "timestamp": datetime.utcnow().isoformat(),
            "reflex": reflex,
            "weights": weight_list,
            "variability": variability,
            "trend": trend
        })

    return results

def main():
    print("📉 Tracking Reflex Convergence...")
    snapshots = load_json(SYNC_LOG_PATH)
    if not snapshots:
        print("[WARN] No reflex sync snapshots found.")
        return

    analysis = analyze_convergence(snapshots)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(analysis, f, indent=4)

    print(f"[TRACK] Convergence report written to {OUTPUT_PATH.name}")

if __name__ == "__main__":
    main()
