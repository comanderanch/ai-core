import json
from pathlib import Path
from datetime import datetime

# ✅ Corrected Paths
RESPONSE_MAP_PATH = Path("memory/trait_response_map.json")
MASTER_LOG_PATH = Path("memory/trait_master_log.json")
OUTPUT_LOG_PATH = Path("memory/trait_response_validation_log.json")

def load_json(path, fallback=None):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return fallback if fallback is not None else {}
    return fallback if fallback is not None else {}

def validate_responses(response_map, master_log):
    validated = []
    unified_traits = master_log.get("unified_traits", {})

    for trait_id, response in response_map.get("responses", {}).items():
        if trait_id in unified_traits:
            validated.append({
                "trait_id": trait_id,
                "response": response,
                "status": "valid"
            })
        else:
            validated.append({
                "trait_id": trait_id,
                "response": response,
                "status": "invalid"
            })

    return validated

def main():
    print("🔍 Validating Trait Responses...")

    response_map = load_json(RESPONSE_MAP_PATH, {})
    master_log = load_json(MASTER_LOG_PATH, {})

    if not response_map or not master_log:
        print("[VALIDATE] Missing required data. Validation skipped.")
        return

    validated = validate_responses(response_map, master_log)

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "validated": validated
    }

    with open(OUTPUT_LOG_PATH, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[VALIDATE] {len(validated)} trait responses validated and saved.")

if __name__ == "__main__":
    main()

