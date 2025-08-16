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
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()

# === EXPORT FUNCTION ===
def hash_token_memory_blocks():
    left_tokens = load_tokens(LEFT_PATH)
    right_tokens = load_tokens(RIGHT_PATH)

    all_blocks = []
    for hemisphere, tokens in [("LEFT", left_tokens), ("RIGHT", right_tokens)]:
        for i in range(0, len(tokens), BLOCK_SIZE):
            block = tokens[i:i+BLOCK_SIZE]
            if block:
                all_blocks.append({
                    "hemisphere": hemisphere,
                    "block": block,
                    "hash": hash_block(block),
                    "timestamp": datetime.utcnow().isoformat()
                })

    HASH_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    if HASH_LOG_PATH.exists():
        with HASH_LOG_PATH.open("r") as f:
            existing = json.load(f)
    else:
        existing = []

    existing.extend(all_blocks)

    with HASH_LOG_PATH.open("w") as f:
        json.dump(existing, f, indent=2)

    print(f"[✓] Hashed {len(all_blocks)} token blocks to {HASH_LOG_PATH}")

# === Main Entry (optional) ===
if __name__ == "__main__":
    hash_token_memory_blocks()
