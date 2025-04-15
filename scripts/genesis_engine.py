import json
import os
from datetime import datetime

ANCHOR_PATH = "memory/core_anchors.json"
GENESIS_PATH = "memory/genesis_proposals.json"

# All known behaviors the system could theoretically use
KNOWN_ACTIONS = [
    "Trigger Action A",
    "Trigger Action B",
    "Trigger Action C",
    "Trigger Action D"
]

def load_anchors():
    if not os.path.exists(ANCHOR_PATH):
        print("[Genesis] No core anchor file found.")
        return []
    with open(ANCHOR_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("[Genesis] Error parsing anchors.")
            return []

def extract_used_actions(anchors):
    used = set()
    for anchor in anchors:
        used.update(anchor.get("based_on", []))
    return used

def generate_behavior_proposals(used_actions):
    proposals = []
    unused = [a for a in KNOWN_ACTIONS if a not in used_actions]

    for action in unused:
        proposal = {
            "suggested_pattern": [action] * 3,
            "reasoning": f"Unused pattern matching anchor structure (x3 repetition of '{action}')",
            "created": datetime.utcnow().isoformat() + "Z"
        }
        proposals.append(proposal)

    return proposals

def save_proposals(proposals):
    with open(GENESIS_PATH, "w") as f:
        json.dump(proposals, f, indent=4)
    print(f"[Genesis] Proposals saved to {GENESIS_PATH}")

def run_genesis_engine():
    print("[Genesis] Running Reflex Expansion Engine...")
    anchors = load_anchors()
    used_actions = extract_used_actions(anchors)
    proposals = generate_behavior_proposals(used_actions)
    save_proposals(proposals)
    print(f"[Genesis] {len(proposals)} new behavior patterns proposed.")

if __name__ == "__main__":
    run_genesis_engine()
