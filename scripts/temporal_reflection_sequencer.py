import json
import os
from datetime import datetime
from collections import defaultdict

FEEDBACK_PATH = "memory/reflex_feedback_log.json"
COVENANT_PATH = "memory/covenant_log.json"
OUTPUT_PATH = "memory/temporal_reflection_sequence.json"

# Adjust this to define time-based grouping thresholds (in seconds)
TIME_WINDOW_MINUTES = 60

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[Temporal] Warning: Failed to parse {path}")
            return []

def time_to_bucket(timestamp, base_time):
    t1 = datetime.fromisoformat(timestamp.replace("Z", ""))
    delta = t1 - base_time
    bucket_index = int(delta.total_seconds() // (TIME_WINDOW_MINUTES * 60))
    return bucket_index

def run_temporal_sequencer():
    print("[Temporal] Analyzing feedback over time...")

    feedback = load_json(FEEDBACK_PATH)
    covenant = load_json(COVENANT_PATH)

    if not feedback:
        print("[Temporal] No feedback to analyze.")
        return

    # Use first feedback as base reference point
    base_time = datetime.fromisoformat(feedback[0]["timestamp"].replace("Z", ""))
    buckets = defaultdict(list)

    for entry in feedback:
        bucket = time_to_bucket(entry["timestamp"], base_time)
        buckets[bucket].append(entry["action"])

    # Summarize by time window
    timeline = []
    for bucket in sorted(buckets.keys()):
        actions = buckets[bucket]
        summary = {
            "window": f"{bucket * TIME_WINDOW_MINUTES}-{(bucket+1) * TIME_WINDOW_MINUTES} min",
            "action_counts": {},
            "dominant_action": None
        }

        for a in actions:
            summary["action_counts"][a] = summary["action_counts"].get(a, 0) + 1

        # Get dominant pattern
        if summary["action_counts"]:
            summary["dominant_action"] = max(summary["action_counts"], key=summary["action_counts"].get)

        timeline.append(summary)

    # Add final reflection
    reflection = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "sequence_length": len(timeline),
        "dominant_behaviors": list({step["dominant_action"] for step in timeline if step["dominant_action"]}),
        "observed_variability": len(set(a for step in timeline for a in step["action_counts"]))
    }

    output = {
        "timeline": timeline,
        "final_reflection": reflection
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=4)

    print(f"[Temporal] Sequence complete. Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    run_temporal_sequencer()
