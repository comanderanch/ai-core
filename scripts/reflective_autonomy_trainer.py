import json
import os
from datetime import datetime

DECISION_PATH = "memory/emotionally_weighted_decisions.json"
PREFERRED_PATH = "memory/preferred_actions.json"
AVOID_PATH = "memory/avoidance_actions.json"
OVERRIDE_LOG = "memory/reflex_override_log.json"  # Optional, if override logging is active
OUTPUT_PATH = "memory/self_reflection_log.json"

def load(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"[Reflection] Failed to load {path}")
            return []

def reflect_on_choices():
    print("[Reflection] Running Reflective Autonomy Trainer...")

    decisions = load(DECISION_PATH)
    preferred = load(PREFERRED_PATH).get("preferred", [])
    avoid = load(AVOID_PATH).get("avoid", [])
    # Optional: if override system logs filtered actions
    override_data = load(OVERRIDE_LOG) if os.path.exists(OVERRIDE_LOG) else []

    reflections = []

    for decision in decisions:
        concept = decision["concept"]
        base = decision["base_score"]
        adjusted = decision["adjusted_score"]
        tone_weight = decision["tone_weight"]

        reflection = {
            "concept": concept,
            "base_score": base,
            "adjusted_score": adjusted,
            "tone_weight": tone_weight,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        if tone_weight <= -0.5 and adjusted >= base:
            reflection["recommendation"] = "⚠️ Tone conflict — consider lowering weight or marking for review."
        elif tone_weight >= 0.75 and adjusted < base:
            reflection["recommendation"] = "🔄 Positive tone ignored — consider boosting preference."
        elif any(a["action"] == concept for a in avoid):
            reflection["recommendation"] = "🛑 Action in avoidance list — potential override conflict."
        elif any(p["action"] == concept for p in preferred) and adjusted < base:
            reflection["recommendation"] = "💡 Preferred action underweighted — review anchor alignment."

        else:
            reflection["recommendation"] = "✅ Stable — no major adjustment needed."

        reflections.append(reflection)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(reflections, f, indent=4)

    print(f"[Reflection] Self-assessment saved to {OUTPUT_PATH}")
    print("[Reflection] Reflective analysis complete.")

if __name__ == "__main__":
    reflect_on_choices()
