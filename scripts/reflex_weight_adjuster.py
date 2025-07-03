import json
from datetime import datetime

REFLEX_SUMMARY_PATH = "memory/reflex_influence_summary.json"
WEIGHT_ADJUSTMENT_LOG = "memory/reflex_weight_adjustments.json"

def adjust_weights():
    with open(REFLEX_SUMMARY_PATH, "r") as f:
        reflex_counts = json.load(f)

    total = sum(reflex_counts.values())
    if total == 0:
        print("[WARN] No reflex influence data to adjust.")
        return

    adjustments = []
    for reflex, count in reflex_counts.items():
        weight = round(count / total, 3)
        adjustments.append({
            "reflex": reflex,
            "adjusted_weight": weight,
            "timestamp": datetime.utcnow().isoformat()
        })
        print(f"[ADJUST] {reflex} ➜ Weight: {weight}")

    with open(WEIGHT_ADJUSTMENT_LOG, "w") as f:
        json.dump(adjustments, f, indent=4)

if __name__ == "__main__":
    adjust_weights()
