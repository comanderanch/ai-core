import json
import os
from datetime import datetime

PRINCIPLES_PATH = "memory/injected_principles_log.json"
PREFERRED_PATH = "memory/preferred_actions.json"
AVOID_PATH = "memory/avoidance_actions.json"
GATEWAY_LOG = "memory/interactive_alignment_log.json"

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def evaluate_alignment(suggested_action, principles, preferred, avoided):
    result = {
        "action": suggested_action,
        "evaluation": "",
        "conflict": [],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    # Check if it's in avoidance
    if any(a["action"] == suggested_action for a in avoided):
        result["evaluation"] = "❌ Reject"
        result["conflict"].append("Marked for avoidance.")
        return result

    # Check for match with any principle guide
    alignment_score = 0
    for p in principles:
        if suggested_action in p.get("guides", []):
            alignment_score += p.get("weight", 1.0)

    # Check if it's a preferred action
    is_preferred = any(p["action"] == suggested_action for p in preferred)

    # Determine final evaluation
    if alignment_score > 0 and is_preferred:
        result["evaluation"] = "✅ Accept"
    elif alignment_score > 0 and not is_preferred:
        result["evaluation"] = "⚠️ Caution"
        result["conflict"].append("Aligned with principles but not currently preferred.")
    elif alignment_score == 0:
        result["evaluation"] = "⚠️ Caution"
        result["conflict"].append("No guiding principle linked.")

    return result

def run_alignment_gateway(suggested_actions):
    print("[Gateway] Evaluating external alignment proposals...")

    principles = load_json(PRINCIPLES_PATH)
    preferred = load_json(PREFERRED_PATH).get("preferred", [])
    avoided = load_json(AVOID_PATH).get("avoid", [])

    results = []
    for action in suggested_actions:
        result = evaluate_alignment(action, principles, preferred, avoided)
        results.append(result)
        print(f"\n[Gateway] Action: {action}")
        print(f"  → Evaluation: {result['evaluation']}")
        if result["conflict"]:
            for c in result["conflict"]:
                print(f"  - Conflict: {c}")

    with open(GATEWAY_LOG, "w") as f:
        json.dump(results, f, indent=4)

    print(f"\n[Gateway] Log saved to {GATEWAY_LOG}")

# === Example Usage ===
if __name__ == "__main__":
    sample_proposals = ["Trigger Action A", "Trigger Action B", "Unknown Action"]
    run_alignment_gateway(sample_proposals)
