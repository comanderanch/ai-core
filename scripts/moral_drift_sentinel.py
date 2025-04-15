import json
import os
from datetime import datetime

PRINCIPLE_LOG = "memory/injected_principles_log.json"
PREFERRED_PATH = "memory/preferred_actions.json"
AVOID_PATH = "memory/avoidance_actions.json"
REFLECTION_PATH = "memory/self_reflection_log.json"
OUTPUT_PATH = "memory/moral_drift_report.json"

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[DriftSentinel] Failed to parse {path}")
            return []

def match_drift(principle, preferences, avoidances, reflections):
    drift_flags = []
    guides = principle.get("guides", [])

    for guide in guides:
        # Check avoidance
        if any(guide == a.get("action") for a in avoidances):
            drift_flags.append(f"🛑 Guide '{guide}' is marked for avoidance.")

        # Check underweight reflections
        for reflect in reflections:
            if guide in reflect.get("context_tokens", []) and "underweighted" in reflect.get("recommendation", "").lower():
                drift_flags.append(f"⚠️ Guide '{guide}' appears in reflection flagged for underweight.")

        # Check missing from preference
        if not any(guide == p.get("action") for p in preferences):
            drift_flags.append(f"ℹ️ Guide '{guide}' missing from current preferred actions.")

    return drift_flags

def run_moral_drift_scan():
    print("[DriftSentinel] Scanning for moral drift...")

    principles = load_json(PRINCIPLE_LOG)
    preferences = load_json(PREFERRED_PATH).get("preferred", [])
    avoidances = load_json(AVOID_PATH).get("avoid", [])
    reflections = load_json(REFLECTION_PATH)

    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "drift_analysis": []
    }

    for principle in principles:
        drift = match_drift(principle, preferences, avoidances, reflections)

        report["drift_analysis"].append({
            "principle": principle["name"],
            "drift_flags": drift if drift else ["✅ No drift detected."]
        })

    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=4)

    print(f"[DriftSentinel] Drift analysis complete. Report saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    run_moral_drift_scan()
