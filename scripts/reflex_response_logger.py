# scripts/reflex_response_logger.py

import json
from memory.label_trait_loader import load_label_trait_map
from datetime import datetime

def simulate_reflex_response(label):
    label_map = load_label_trait_map()
    trait_info = label_map.get(label)

    if not trait_info:
        print(f"[ERROR] Label '{label}' not recognized.")
        return

    reflex = trait_info["reflex_trigger"]
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "label": label,
        "reflex": reflex,
        "trait": trait_info["trait"]
    }

    with open("memory/reflex_response_log.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"[LOG] Reflex triggered for '{label}': {reflex}")

# Example usage
if __name__ == "__main__":
    simulate_reflex_response("Growth")
