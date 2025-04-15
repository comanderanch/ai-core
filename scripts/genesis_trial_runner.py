import json
import os
from datetime import datetime
from behavior_trigger_system import trigger_from_tokens
from decision_chain_manager import construct_from_reflex

GENESIS_PATH = "memory/genesis_proposals.json"
REFLEX_LOG_PATH = "memory/reflex_feedback_log.json"
TRIAL_REPORT_PATH = "memory/genesis_trial_log.json"

def load_json(path):
    if not os.path.exists(path):
        print(f"[TrialRunner] Missing file: {path}")
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[TrialRunner] Corrupted JSON in {path}")
            return []

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def append_reflex_log(action):
    reflex_log = load_json(REFLEX_LOG_PATH)
    entry = {
        "action": action,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    reflex_log.append(entry)
    save_json(reflex_log, REFLEX_LOG_PATH)
    print(f"[TrialRunner] Injected reflex action: {action}")

def run_genesis_trial():
    print("[TrialRunner] Starting Genesis Trial...")

    proposals = load_json(GENESIS_PATH)
    if not proposals:
        print("[TrialRunner] No proposals available.")
        return

    trial_pattern = proposals[0]["suggested_pattern"]
    print(f"[TrialRunner] Trial Pattern: {trial_pattern}")

    for action in trial_pattern:
        append_reflex_log(action)

    # Activate system behavior & cognition
    print("[TrialRunner] Running behavior and cognition...")
    trigger_tokens = []
    if "Trigger Action A" in trial_pattern:
        trigger_tokens.append(20)
    if "Trigger Action B" in trial_pattern:
        trigger_tokens.append(40)
    if "Trigger Action C" in trial_pattern:
        trigger_tokens.append(60)
    if "Trigger Action D" in trial_pattern:
        trigger_tokens.append(80)

    trigger_from_tokens(trigger_tokens)
    construct_from_reflex(trigger_tokens)

    # Trial log
    trial_record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "executed_pattern": trial_pattern,
        "origin": "genesis_proposals.json",
        "status": "Trial complete. Awaiting alignment scoring."
    }

    save_json(trial_record, TRIAL_REPORT_PATH)
    print("[TrialRunner] Trial logged. Run Manifest Guardian to evaluate impact.")

if __name__ == "__main__":
    run_genesis_trial()
