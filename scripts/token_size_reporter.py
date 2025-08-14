# token_size_reporter.py
# Phase 39.3 – Reports token set sizes, memory hash block count, and estimated memory footprint

import os
import json
from pathlib import Path

LEFT_PATH = Path("tokenizer/token_set_left.json")
RIGHT_PATH = Path("tokenizer/token_set_right.json")
HASH_PATH = Path("memory/snapshots/token_hash_log.json")

# === Helpers ===
def count_tokens(path):
    if not path.exists():
        return 0
    with path.open("r") as f:
        return len(json.load(f))

def count_hashes(path):
    if not path.exists():
        return 0
    with path.open("r") as f:
        return len(json.load(f))

def get_file_size_kb(path):
    if not path.exists():
        return 0
    return os.path.getsize(path) / 1024

# === Report Generator ===
def report():
    left_tokens = count_tokens(LEFT_PATH)
    right_tokens = count_tokens(RIGHT_PATH)
    hash_blocks = count_hashes(HASH_PATH)

    size_left = get_file_size_kb(LEFT_PATH)
    size_right = get_file_size_kb(RIGHT_PATH)
    size_hash = get_file_size_kb(HASH_PATH)

    print("\n🧠 Token Memory Size Report")
    print("----------------------------")
    print(f"Left Tokens      : {left_tokens}  | {size_left:.2f} KB")
    print(f"Right Tokens     : {right_tokens}  | {size_right:.2f} KB")
    print(f"Hash Blocks      : {hash_blocks}   | {size_hash:.2f} KB")
    print("----------------------------")
    print(f"Total Token Count: {left_tokens + right_tokens}")
    print(f"Approx Memory Use: {size_left + size_right + size_hash:.2f} KB\n")

if __name__ == "__main__":
    report()
