import json
import os
from collections import defaultdict

# File paths
FEEDBACK_LOG = "memory/reflex_feedback_log.json"
SUMMARY_LOG = "memory/reflex_behavior_summary.json"

def load_feedback():
    if not os.path.exists(FEEDBACK_LOG):
        print("[Analyzer] No feedback log found.")
        return []

    with open(FEEDBACK_LOG, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("[Analyzer] Warning: feedback log is invalid JSON.")
            return []

def analyze_feedback(feedback_entries):
    summary = defaultdict(int)
    for entry in feedback_entries:
        action = entry.get("action", "Unknown Action")
        summary[action] += 1
    return summary

def save_summary(summary):
    summary_list = [{"action": action, "count": count} for action, count in summary.items()]
    with open(SUMMARY_LOG, "w") as f:
        json.dump(summary_list, f, indent=4)
    print(f"[Analyzer] Summary saved to {SUMMARY_LOG}")

def run_feedback_analysis():
    print("[Analyzer] Running Reflex Feedback Analysis...")
    feedback_entries = load_feedback()
    summary = analyze_feedback(feedback_entries)
    save_summary(summary)

if __name__ == "__main__":
    run_feedback_analysis()
