import json
import os
from collections import defaultdict, Counter
from datetime import datetime

# File paths
FEEDBACK_LOG_PATH = "memory/reflex_feedback_log.json"
ECHO_MAP_PATH = "memory/cognitive_echo_map.json"

# How many recent actions to treat as a "pattern"
PATTERN_WINDOW_SIZE = 3

def load_feedback_log():
    if not os.path.exists(FEEDBACK_LOG_PATH):
        print("[Echo Mapper] No feedback log found.")
        return []

    with open(FEEDBACK_LOG_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("[Echo Mapper] Warning: feedback log is invalid.")
            return []

def extract_action_sequence(feedback_entries):
    return [entry.get("action", "Unknown Action") for entry in feedback_entries]

def detect_repeating_patterns(sequence, window_size):
    pattern_counter = Counter()
    for i in range(len(sequence) - window_size + 1):
        window = tuple(sequence[i:i+window_size])
        pattern_counter[window] += 1
    return pattern_counter

def save_echo_map(echo_map):
    mapped = []
    for pattern, count in echo_map.items():
        mapped.append({
            "pattern": list(pattern),
            "count": count
        })

    with open(ECHO_MAP_PATH, "w") as f:
        json.dump(mapped, f, indent=4)
    print(f"[Echo Mapper] Cognitive echo map saved to {ECHO_MAP_PATH}")

def run_echo_mapping():
    print("[Echo Mapper] Starting Cognitive Echo Mapping...")

    feedback_log = load_feedback_log()
    sequence = extract_action_sequence(feedback_log)

    if len(sequence) < PATTERN_WINDOW_SIZE:
        print("[Echo Mapper] Not enough data to detect patterns.")
        return

    echo_patterns = detect_repeating_patterns(sequence, PATTERN_WINDOW_SIZE)
    save_echo_map(echo_patterns)

    print("[Echo Mapper] Echo detection complete.")

if __name__ == "__main__":
    run_echo_mapping()
