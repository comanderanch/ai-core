# hash_token_memory.py
# Phase 39.2 – Hashes token memory blocks for recall, tracking, and size analysis

import hashlib
import json
from pathlib import Path
from datetime import datetime

# === Config ===
LEFT_PATH = Path("tokenizer/token_set_left.json")
RIGHT_PATH = Path("tokenizer/token_set_right.json")
HASH_LOG_PATH = Path("memory/snapshots/token_hash_log.json")
BLOCK_SIZE = 10  # Number of tokens per hash block

# === Helpers ===
def load_tokens(path):
    if not path.exists():
        return []
    with path.open("r") as f:
        return json.load(f)

def hash_block(block):
    joined = " ".join(block)
    return hashlib.sha256(joined.encode()).hexdigest()

def process_tokens(tokens, hemisphere):
    hashes = []
    for i in range(0, len(tokens), BLOCK_SIZE):
        block = tokens[i:i+BLOCK_SIZE]
        if len(block) < BLOCK_SIZE:
            continue
        block_hash = hash_block(block)
        hashes.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "hemisphere": hemisphere,
            "block_index": i // BLOCK_SIZE,
            "token_count": len(block),
            "hash": block_hash
        })
    return hashes

def save_hash_log(entries):
    existing = []
    if HASH_LOG_PATH.exists():
        with HASH_LOG_PATH.open("r") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []

    existing.extend(entries)
    with HASH_LOG_PATH.open("w") as f:
        json.dump(existing, f, indent=2)

# === Main Hashing Function ===
def hash_all_memory():
    left_tokens = load_tokens(LEFT_PATH)
    right_tokens = load_tokens(RIGHT_PATH)

    all_hashes = []
    all_hashes.extend(process_tokens(left_tokens, "left"))
    all_hashes.extend(process_tokens(right_tokens, "right"))

    save_hash_log(all_hashes)
    print(f"[✓] Hashed {len(all_hashes)} token blocks to memory/snapshots/token_hash_log.json")

if __name__ == "__main__":
    hash_all_memory()
