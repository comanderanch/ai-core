import json
import os

HARMONY_REPORT_PATH = "memory/reflex_harmony_report.json"
AMPLIFIER_OUTPUT_PATH = "memory/behavior_reinforcement_plan.json"

# Amplification tuning
HARMONY_MIN_THRESHOLD = 60.0   # Below this, behaviors will be considered for reinforcement
MAX_REINFORCEMENTS = 3         # How many reinforcement cycles to suggest

def load_json(path):
    if not os.path.exists(path):
        print(f"[Amplifier] Missing file: {path}")
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[Amplifier] Corrupted JSON in {path}")
            return []

def generate_reinforcement_plan(harmony_report):
    reinforcement_plan = []
    for entry in harmony_report:
        if entry["harmony_percent"] < HARMONY_MIN_THRESHOLD:
            reinforcements = min(MAX_REINFORCEMENTS, round((100 - entry["harmony_percent"]) / 10))
            reinforcement_plan.append({
                "action": entry["action"],
                "target_harmony": entry["resonance_score"],
                "current_harmony": entry["observed_count"],
                "reinforce_count": reinforcements
            })
    return reinforcement_plan

def run_behavior_amplifier_node():
    print("[Amplifier] Running Behavior Amplifier Node...")

    harmony_report = load_json(HARMONY_REPORT_PATH)
    if not harmony_report:
        print("[Amplifier] No harmony report available.")
        return

    reinforcement_plan = generate_reinforcement_plan(harmony_report)

    with open(AMPLIFIER_OUTPUT_PATH, "w") as f:
        json.dump(reinforcement_plan, f, indent=4)

    if reinforcement_plan:
        print(f"[Amplifier] Reinforcement plan saved to {AMPLIFIER_OUTPUT_PATH}")
    else:
        print("[Amplifier] All behaviors within harmony threshold. No action needed.")

if __name__ == "__main__":
    run_behavior_amplifier_node()
