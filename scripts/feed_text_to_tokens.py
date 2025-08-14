# feed_text_to_tokens.py
# Phase 39.1 – Convert book or text file to token stream for hemisphere sets

import json
from pathlib import Path
import re

# === Config ===
LEFT_PATH = Path("tokenizer/token_set_left.json")
RIGHT_PATH = Path("tokenizer/token_set_right.json")

# === Token Conversion Placeholder ===
def tokenize_text_block(block):
    words = re.findall(r"\b\w+\b", block.lower())
    return [f"{word}_{i}" for i, word in enumerate(words)]

# === Loader/Saver ===
def load_tokens(path):
    if not path.exists():
        return []
    with path.open("r") as f:
        return json.load(f)

def save_tokens(path, tokens):
    with path.open("w") as f:
        json.dump(tokens, f, indent=2)

# === Main Feed Function ===
def feed_text_file(file_path, hemisphere="left", chunk_size=1):
    target = LEFT_PATH if hemisphere == "left" else RIGHT_PATH
    current = load_tokens(target)

    with open(file_path, "r") as f:
        text = f.read()

    blocks = re.split(r"\n\n+|(?<=[.!?])\s+", text)
    fed = 0

    for block in blocks:
        if not block.strip():
            continue
        tokens = tokenize_text_block(block)
        current.extend(tokens)
        fed += 1
        if fed >= chunk_size:
            break

    save_tokens(target, current)
    print(f"[✓] Appended {fed} block(s) to {hemisphere.upper()} hemisphere.")
    print(f"[→] Total tokens in {hemisphere.upper()}: {len(current)}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 feed_text_to_tokens.py <path/to/textfile> [left|right] [chunk_size]")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    hemisphere = sys.argv[2] if len(sys.argv) > 2 else "left"
    chunk = int(sys.argv[3]) if len(sys.argv) > 3 else 1

    feed_text_file(filepath, hemisphere, chunk)
