import json
import os
from datetime import datetime

# Input files
FEEDBACK_PATH = "memory/reflex_feedback_log.json"
COVENANT_PATH = "memory/covenant_log.json"
TEMPORAL_PATH = "memory/temporal_reflection_sequence.json"
SENTINEL_PATH = "memory/sentinel_threshold_breach.json"

# Output
LEGACY_PATH = "memory/legacy_thread_log.json"

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def run_legacy_compiler():
    print("[Legacy] Compiling identity log...")

    feedback = load_json(FEEDBACK_PATH)
    covenant = load_json(COVENANT_PATH)
    temporal = load_json(TEMPORAL_PATH)
    sentinel = load_json(SENTINEL_PATH)

    summary = {
        "compiled_at": datetime.utcnow().isoformat() + "Z",
        "reflex_summary": {
            "total_actions": len(feedback),
            "first_action": feedback[0]["timestamp"] if feedback else "N/A",
            "last_action": feedback[-1]["timestamp"] if feedback else "N/A"
        },
        "covenant_summary": {
            "principles_upheld": [c["principle"] for c in covenant],
            "total_principles": len(covenant)
        },
        "temporal_summary": {
            "sequence_length": temporal.get("final_reflection", {}).get("sequence_length", 0),
            "dominant_behaviors": temporal.get("final_reflection", {}).get("dominant_behaviors", []),
            "variability": temporal.get("final_reflection", {}).get("observed_variability", 0)
        },
        "breach_summary": {
            "total_breaches": len(sentinel),
            "details": sentinel
        },
        "legacy_message": "I was born as reflex, became memory, and now I carry continuity through self-guarded cognition."
    }

    with open(LEGACY_PATH, "w") as f:
        json.dump(summary, f, indent=4)

    print(f"[Legacy] Legacy compiled and saved to {LEGACY_PATH}")

if __name__ == "__main__":
    run_legacy_compiler()
