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
def report_token_memory_size(print_report=True):
    left_tokens = count_tokens(LEFT_PATH)
    right_tokens = count_tokens(RIGHT_PATH)
    hash_blocks = count_hashes(HASH_PATH)
    total_tokens = left_tokens + right_tokens
    approx_memory_kb = round(((left_tokens + right_tokens + hash_blocks) * 16) / 1024, 2)

    if print_report:
        print("🧠 Token Memory Size Report")
        print("----------------------------")
        print(f"Left Tokens      : {left_tokens}  | {round(left_tokens * 16 / 1024, 2)} KB")
        print(f"Right Tokens     : {right_tokens}  | {round(right_tokens * 16 / 1024, 2)} KB")
        print(f"Hash Blocks      : {hash_blocks}   | {round(hash_blocks * 16 / 1024, 2)} KB")
        print("----------------------------")
        print(f"Total Token Count: {total_tokens}")
        print(f"Approx Memory Use: {approx_memory_kb} KB\n")

    return {
        "left_tokens": left_tokens,
        "right_tokens": right_tokens,
        "hash_blocks": hash_blocks,
        "total_tokens": total_tokens,
        "approx_memory_kb": approx_memory_kb
    }
