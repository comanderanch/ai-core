import json
from pathlib import Path
from datetime import datetime

# === Paths ===
MASTER_LOG = Path("memory/trait_master_log.json")
PRIORITY_MAP = Path("memory/trait_priority_map.json")
ANCHOR_STABILITY_LOG = Path("memory/trait_anchor_stability_log.json")
OUTPUT_PATH = Path("memory/trait_response_map.json")

# === Load utility ===
def load_json(path, fallback):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return fallback
    return fallback

# === Trait Response Synthesizer ===
def synthesize_responses(master, priorities, anchors):
    response_map = {}

    for trait_id, data in master.get("unified_traits", {}).items():
        bias = data.get("bias", 0)
        weight = data.get("weight", 0)
        priority = priorities.get("priority_scores", {}).get(trait_id, 0)
        anchor_data = next((entry for entry in anchors if entry.get("trait_id") == trait_id), None)
        stability_score = anchor_data.get("stability_score", 0) if anchor_data else 0

        # Simple weighted average response formula
        response_strength = round((bias + weight + priority + stability_score) / 4, 4)

        response_map[trait_id] = {
            "bias": bias,
            "weight": weight,
            "priority": priority,
            "stability_score": stability_score,
            "response_strength": response_strength
        }

    return response_map

# === Main ===
def main():
    print("🧠 Synthesizing Trait Responses...")

    master_log = load_json(MASTER_LOG, {})
    priority_map = load_json(PRIORITY_MAP, {})
    anchor_log = load_json(ANCHOR_STABILITY_LOG, [])

    if not master_log or not priority_map or not anchor_log:
        print("[RESPONSE] Missing input logs. Synthesis aborted.")
        return

    responses = synthesize_responses(master_log, priority_map, anchor_log)

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "responses": responses
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[RESPONSE] {len(responses)} trait responses synthesized.")

if __name__ == "__main__":
    main()
