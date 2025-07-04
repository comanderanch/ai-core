# scripts/trait_stability_summarizer.py

import json
from pathlib import Path
from datetime import datetime

# Paths
ANCHOR_LOG_PATH = Path("memory/trait_anchor_stability_log.json")
EQUILIBRIUM_PATH = Path("memory/trait_equilibrium_log.json")
OUTPUT_PATH = Path("memory/trait_stability_summary.json")

def load_json(path, fallback=[]):
    if path.exists():
        try:
            with open(path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return fallback
    return fallback

def summarize_stability(anchor_log, equilibrium_log):
    stability_summary = {}

    # Organize equilibrium log for quick lookup
    eq_map = equilibrium_log.get("summary", {})


    for anchor in anchor_log:
        trait_id = anchor["trait_id"]
        equilibrium = eq_map.get(trait_id, {})

        stability_summary[trait_id] = {
            "bias": anchor["bias"],
            "weight": anchor["weight"],
            "drift": anchor["drift"],
            "stability_score": anchor["stability_score"],
            "state": anchor["state"],
            "equilibrium_deviation": equilibrium.get("deviation", None),
            "equilibrium_state": equilibrium.get("state", None)
        }

    return stability_summary

def main():
    print("📊 Summarizing Trait Stability...")

    anchor_log = load_json(ANCHOR_LOG_PATH)
    equilibrium_log = load_json(EQUILIBRIUM_PATH)

    if not anchor_log:
        print("[STABILITY] No anchor log data found. Summary skipped.")
        return

    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "stability_summary": summarize_stability(anchor_log, equilibrium_log)
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(summary, f, indent=4)

    print(f"[STABILITY] Stability summary saved for {len(summary['stability_summary'])} traits.")

if __name__ == "__main__":
    main()
