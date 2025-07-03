# scripts/reflex_drift_handler.py

import json
from pathlib import Path
from datetime import datetime

RESPONSE_LOG = Path("memory/reflex_response_log.json")
BIAS_LOG = Path("memory/memory_bias_log.json")
WEIGHT_LOG = Path("memory/reflex_weight_log.json")
DRIFT_LOG = Path("memory/reflex_drift_log.json")

def load_json(path):
    if not path.exists():
        return None
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def main():
    response = load_json(RESPONSE_LOG)
    bias_entries = load_json(BIAS_LOG)
    weights = load_json(WEIGHT_LOG)
    drift_log = load_json(DRIFT_LOG) or []

    if not response or not bias_entries or not weights:
        print("[DRIFT] Missing required data. Drift check skipped.")
        return

    label = response.get("label")
    reflex = response.get("reflex")

    bias_map = {entry["label"]: entry["bias"] for entry in bias_entries if "label" in entry and "bias" in entry}

    if label not in bias_map or reflex not in weights:
        print("[DRIFT] Reflex or label not found. Drift check skipped.")
        return

    bias = bias_map[label]
    weight = weights[reflex]
    drift = round(weight - bias, 3)

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "label": label,
        "reflex": reflex,
        "bias": bias,
        "weight": weight,
        "drift": drift
    }

    drift_log.append(entry)
    save_json(DRIFT_LOG, drift_log)

    print(f"[DRIFT] Reflex '{reflex}' drift recorded: {drift:+}")

if __name__ == "__main__":
    main()
