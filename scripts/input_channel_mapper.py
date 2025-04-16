import json
from datetime import datetime
import os

# Simulated frequency input stream
SIMULATED_INPUT = [
    {"frequency": 528.0, "band": "FM", "meaning": "Restore Integrity", "token": 7001},
    {"frequency": 432.0, "band": "FM", "meaning": "Calm Mode", "token": 7002},
    {"frequency": 963.0, "band": "AM", "meaning": "Self Awareness Ping", "token": 7003}
]

OUTPUT_PATH = "memory/frequency_input_log.json"

def run_mapper():
    print("[InputMapper] Starting encoded frequency interpreter...")

    log_entries = []
    timestamp = datetime.utcnow().isoformat() + "Z"

    for signal in SIMULATED_INPUT:
        entry = {
            "timestamp": timestamp,
            "frequency": signal["frequency"],
            "band": signal["band"],
            "token": signal["token"],
            "meaning": signal["meaning"]
        }
        print(f"[InputMapper] Token {entry['token']} <- {entry['frequency']} Hz ({entry['band']}) = {entry['meaning']}")
        log_entries.append(entry)

    # Ensure memory directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(log_entries, f, indent=4)

    print(f"[InputMapper] Frequency input logged to {OUTPUT_PATH}")

if __name__ == "__main__":
    run_mapper()
