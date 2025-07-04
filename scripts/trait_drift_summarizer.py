# scripts/trait_drift_summarizer.py

import json
from pathlib import Path
from datetime import datetime

# Paths
DRIFT_LOG_PATH = Path("memory/trait_drift_log.json")
OUTPUT_SUMMARY_PATH = Path("memory/trait_drift_summary.json")

def load_json(path, fallback):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return fallback
    return fallback

def summarize_drift(drift_log):
    summary = {}
    for entry in drift_log:
        trait_id = entry.get("trait_id")
        drift = entry.get("drift", 0.0)
        if not trait_id:
            continue
        if trait_id not in summary:
            summary[trait_id] = {
                "total_drift": 0.0,
                "entries": 0
            }
        summary[trait_id]["total_drift"] += drift
        summary[trait_id]["entries"] += 1

    for trait_id, data in summary.items():
        data["average_drift"] = round(data["total_drift"] / data["entries"], 4)

    return summary

def main():
    print("📊 Summarizing Trait Drift...")
    drift_log = load_json(DRIFT_LOG_PATH, [])
    if not drift_log:
        print("[SUMMARY] No drift log data found. Summary skipped.")
        return

    summary = summarize_drift(drift_log)

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "summary": summary
    }

    with open(OUTPUT_SUMMARY_PATH, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[SUMMARY] Drift summary written for {len(summary)} trait(s).")

if __name__ == "__main__":
    main()
