import json
import os
from datetime import datetime

PRINCIPLE_LOG = "memory/injected_principles_log.json"
PREFERENCE_PATH = "memory/preferred_actions.json"
FEEDBACK_PATH = "memory/reflex_feedback_log.json"
COVENANT_PATH = "memory/covenant_log.json"

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[Covenant] Warning: Failed to parse {path}")
            return []

def extract_kept_principles(principles, feedback, preferred):
    covenant = []
    preferred_actions = {p['action'] for p in preferred.get("preferred", [])}
    action_counts = {}

    for entry in feedback:
        action = entry.get("action")
        if action:
            action_counts[action] = action_counts.get(action, 0) + 1

    for principle in principles:
        aligned_actions = [a for a in principle.get("guides", []) if a in preferred_actions or action_counts.get(a, 0) > 0]

        if aligned_actions:
            covenant.append({
                "principle": principle["name"],
                "upheld_guides": aligned_actions,
                "upheld_count": sum(action_counts.get(a, 0) for a in aligned_actions),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })

    return covenant

def run_covenant_archive():
    print("[Covenant] Evaluating memory for honored principles...")

    principles = load_json(PRINCIPLE_LOG)
    feedback = load_json(FEEDBACK_PATH)
    preferred = load_json(PREFERENCE_PATH)

    covenant_entries = extract_kept_principles(principles, feedback, preferred)

    with open(COVENANT_PATH, "w") as f:
        json.dump(covenant_entries, f, indent=4)

    print(f"[Covenant] {len(covenant_entries)} principles honored and archived.")
    print(f"[Covenant] Log saved to {COVENANT_PATH}")

if __name__ == "__main__":
    run_covenant_archive()
