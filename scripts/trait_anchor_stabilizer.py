import json
from pathlib import Path
from datetime import datetime

ANCHOR_LOG_PATH = Path("memory/trait_anchor_reinforcement_log.json")
MASTER_LOG_PATH = Path("memory/trait_master_log.json")
OUTPUT_LOG_PATH = Path("memory/trait_anchor_stability_log.json")

def load_json(path, fallback):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return fallback
    return fallback

def stabilize_anchors(anchor_log, master_log):
    results = []

    for entry in anchor_log:
        trait_id = entry.get("trait_id")
        old_weight = entry.get("old_weight", 0.0)
        new_weight = entry.get("new_weight", 0.0)
        stability_score = entry.get("stability_score", 1.0)

        if trait_id not in master_log.get("unified_traits", {}):
            continue

        trait_data = master_log["unified_traits"][trait_id]
        bias = trait_data.get("bias", 0.0)
        drift = round(abs(new_weight - bias), 4)

        state = "stable"
        if drift > 0.15:
            state = "critical"
        elif drift > 0.05:
            state = "warning"

        results.append({
            "timestamp": datetime.utcnow().isoformat(),
            "trait_id": trait_id,
            "bias": bias,
            "weight": new_weight,
            "drift": drift,
            "stability_score": stability_score,
            "state": state
        })

    return results

def main():
    print("🧷 Running Trait Anchor Stabilizer...")

    anchor_log = load_json(ANCHOR_LOG_PATH, [])
    master_log = load_json(MASTER_LOG_PATH, {})

    if not anchor_log or not master_log:
        print("[ANCHOR-STABILIZE] Missing data. Stabilization skipped.")
        return

    results = stabilize_anchors(anchor_log, master_log)

    with open(OUTPUT_LOG_PATH, "w") as f:
        json.dump(results, f, indent=4)

    print(f"[ANCHOR-STABILIZE] {len(results)} anchors evaluated and saved.")

if __name__ == "__main__":
    main()
