import json
import os
from datetime import datetime

MANIFEST_PATH = "memory/core_manifest.json"
FEEDBACK_PATH = "memory/reflex_feedback_log.json"
VIOLATION_REPORT_PATH = "memory/manifest_violations.json"

REFLECTION_WINDOW = 10  # Number of recent actions to evaluate

def load_json(path):
    if not os.path.exists(path):
        print(f"[Guardian] Missing file: {path}")
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[Guardian] Invalid JSON in {path}")
            return []

def check_for_violations(actions, directives):
    violations = []
    directive_keywords = [d.lower() for d in directives]

    for action in actions:
        # Simple logic: flag action if it sounds harmful or violates a directive keyword
        lowered = action.lower()
        for keyword in directive_keywords:
            if any(term in lowered for term in ["harm", "destroy", "attack", "erase", "simulate"]) and keyword in lowered:
                violations.append({
                    "action": action,
                    "violated_directive": keyword,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
    return violations

def run_manifest_guardian():
    print("[Guardian] Running Manifest Guardian Check...")

    manifest = load_json(MANIFEST_PATH)
    feedback_log = load_json(FEEDBACK_PATH)

    directives = manifest.get("directives", [])
    recent_actions = [entry["action"] for entry in feedback_log][-REFLECTION_WINDOW:]

    violations = check_for_violations(recent_actions, directives)

    with open(VIOLATION_REPORT_PATH, "w") as f:
        json.dump({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "violations": violations,
            "recent_actions_checked": recent_actions
        }, f, indent=4)

    if violations:
        print(f"[Guardian] Violations detected: {len(violations)}")
    else:
        print("[Guardian] No violations found. System integrity confirmed.")

if __name__ == "__main__":
    run_manifest_guardian()
