import json
from datetime import datetime, timedelta
from pathlib import Path

# Paths
RESPONSE_LOG = Path("memory/reflex_response_log.json")
WEIGHT_LOG = Path("memory/reflex_weight_log.json")
DECAY_LOG = Path("memory/reflex_decay_log.json")

# Decay settings
DECAY_THRESHOLD_HOURS = 6  # How long before decay kicks in
DECAY_RATE = 0.05          # How much to decay per threshold

def load_json(path, default):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def apply_decay(reflex, last_timestamp, weight_map):
    now = datetime.utcnow()
    last_time = datetime.fromisoformat(last_timestamp)
    hours_passed = (now - last_time).total_seconds() / 3600

    if hours_passed < DECAY_THRESHOLD_HOURS:
        return weight_map[reflex], False

    decay_steps = int(hours_passed // DECAY_THRESHOLD_HOURS)
    new_weight = weight_map[reflex] * ((1.0 - DECAY_RATE) ** decay_steps)
    new_weight = max(0.1, round(new_weight, 3))  # Don't go below 0.1

    return new_weight, True

def main():
    reflex_log = load_json(RESPONSE_LOG, {})
    weight_map = load_json(WEIGHT_LOG, {})
    decay_events = load_json(DECAY_LOG, [])

    reflex = reflex_log.get("reflex")
    timestamp = reflex_log.get("timestamp")

    if not reflex or reflex not in weight_map or not timestamp:
        print("[DECAY] Missing required data. Decay skipped.")
        return

    new_weight, decayed = apply_decay(reflex, timestamp, weight_map)

    if decayed:
        decay_events.append({
            "timestamp": datetime.utcnow().isoformat(),
            "reflex": reflex,
            "old_weight": weight_map[reflex],
            "new_weight": new_weight
        })
        weight_map[reflex] = new_weight
        save_json(WEIGHT_LOG, weight_map)
        save_json(DECAY_LOG, decay_events)
        print(f"[DECAY] Reflex '{reflex}' decayed to {new_weight}")
    else:
        print(f"[DECAY] Reflex '{reflex}' is recent. No decay applied.")

if __name__ == "__main__":
    main()
