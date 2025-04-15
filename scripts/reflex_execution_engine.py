import sys
import os
import json

# Patch system path so sibling imports work when not run as a package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import behavior_trigger_system


DECISION_MATRIX_PATH = "memory/decision_matrix.json"

def load_json(path):
    if not os.path.exists(path):
        print(f"[Execution] Missing file: {path}")
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[Execution] Corrupted JSON in {path}")
            return []

def execute_top_decision(decision_matrix):
    if not decision_matrix:
        print("[Execution] No decisions available.")
        return

    top_decision = decision_matrix[0]  # Highest score
    concept = top_decision["concept"]
    tokens = top_decision["context_tokens"]

    print(f"[Execution] Executing concept: {concept}")
    print(f"[Execution] Using tokens: {tokens}")
    behavior_trigger_system.trigger_from_tokens([20 if "Trigger Action A" in tokens else 40])

def run_reflex_execution_engine():
    print("[Execution] Starting Reflex Execution Engine...")

    decision_matrix = load_json(DECISION_MATRIX_PATH)
    if not decision_matrix:
        print("[Execution] No decision matrix found.")
        return

    execute_top_decision(decision_matrix)

    print("[Execution] Reflex action complete.")

if __name__ == "__main__":
    run_reflex_execution_engine()
