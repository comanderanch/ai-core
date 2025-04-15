# scripts/cognitive_reflex_engine.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from memory import token_trail
from scripts import token_reflex_loop, behavior_trigger_system, decision_chain_manager

# File paths
REFLEX_PATH = "memory/reflex_tokens_log.json"
TRAIL_PATH = "memory/token_trail_log.json"

def load_json(path):
    with open(path, "r") as file:
        return json.load(file)

def analyze_reflex_tokens(reflex_data):
    # Threshold reflex count to qualify for cognitive response
    THRESHOLD = 2
    return [entry["token"] for entry in reflex_data if entry["count"] >= THRESHOLD]

def activate_behavior_triggers(reflexive_tokens):
    print(f"[Cognition] Activating behavior triggers for tokens: {reflexive_tokens}")
    behavior_trigger_system.trigger_from_tokens(reflexive_tokens)

def build_decision_chains(tokens):
    print(f"[Cognition] Building decision chains for tokens: {tokens}")
    decision_chain_manager.construct_from_reflex(tokens)

def run_cognitive_reflex_engine():
    print("[Cognition] Starting Reflex Engine")

    reflex_data = load_json(REFLEX_PATH)
    trail_data = load_json(TRAIL_PATH)

    reflexive_tokens = analyze_reflex_tokens(reflex_data)

    activate_behavior_triggers(reflexive_tokens)
    build_decision_chains(reflexive_tokens)

    print("[Cognition] Reflex Engine Complete")

if __name__ == "__main__":
    run_cognitive_reflex_engine()
