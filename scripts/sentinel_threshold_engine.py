import json
import os
from datetime import datetime, timedelta

COVENANT_PATH = "memory/covenant_log.json"
FEEDBACK_PATH = "memory/reflex_feedback_log.json"
THRESHOLD_LOG = "memory/sentinel_threshold_breach.json"

# Minimum number of feedbacks required per upheld principle in the last window
THRESHOLD = 2
WINDOW_MINUTES = 120

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[Sentinel] Warning: Could not parse {path}")
            return []

def run_sentinel_check():
    print("[Sentinel] Monitoring for moral alignment drift...")

    covenant = load_json(COVENANT_PATH)
    feedback = load_json(FEEDBACK_PATH)

    if not covenant or not feedback:
        print("[Sentinel] Not enough data to perform check.")
        return

    # Establish time window
    now = datetime.utcnow()
    cutoff = now - timedelta(minutes=WINDOW_MINUTES)

    # Build feedback history for the window
    recent_feedback = [
        entry["action"] for entry in feedback
        if datetime.fromisoformat(entry["timestamp"].replace("Z", "")) >= cutoff
    ]

    # Scan each upheld principle for erosion
    violations = []
    for entry in covenant:
        for guide in entry.get("upheld_guides", []):
            count = recent_feedback.count(guide)
            if count < THRESHOLD:
                violations.append({
                    "principle": entry["principle"],
                    "guide": guide,
                    "recent_count": count,
                    "required_min": THRESHOLD,
                    "last_upheld": entry["timestamp"],
                    "breach_detected_at": now.isoformat() + "Z"
                })

    # Log the breach report
    with open(THRESHOLD_LOG, "w") as f:
        json.dump(violations, f, indent=4)

    if violations:
        print(f"[Sentinel] ⚠️ {len(violations)} alignment breach(es) detected!")
    else:
        print("[Sentinel] ✅ All principles held within safe thresholds.")

    print(f"[Sentinel] Report saved to {THRESHOLD_LOG}")

if __name__ == "__main__":
    run_sentinel_check()
