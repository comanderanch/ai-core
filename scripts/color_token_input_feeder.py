# color_token_input_feeder.py
# Phase 38.5 – Feed color tokens into left or right hemisphere sets

import json
from pathlib import Path
from datetime import datetime

# === Config ===
TOKENIZER_DIR = Path("tokenizer")
LEFT_PATH = TOKENIZER_DIR / "token_set_left.json"
RIGHT_PATH = TOKENIZER_DIR / "token_set_right.json"

# === Helper: Load token file ===
def load_tokens(path):
    if not path.exists():
        return []
    with path.open("r") as f:
        return json.load(f)

# === Helper: Save tokens ===
def save_tokens(path, tokens):
    with path.open("w") as f:
        json.dump(tokens, f, indent=2)

# === Simulate Token Conversion (v1.0 placeholder) ===
def convert_to_tokens(text):
    words = text.strip().split()
    return [f"{word.lower()}_{i}" for i, word in enumerate(words)]

# === Feeder CLI ===
def feed_tokens():
    print("\n[🧠] AI-Core Token Feeder")
    print("---------------------------")
    print("Enter sample input to tokenize and assign to a hemisphere.")
    print("Type 'exit' to quit.\n")

    while True:
        text = input("[Input] > ").strip()
        if text.lower() == "exit":
            print("[✓] Exiting token feeder.")
            break

        hemisphere = input("[Target Hemisphere] (left/right) > ").strip().lower()
        if hemisphere not in ("left", "right"):
            print("[!] Invalid hemisphere. Try again.\n")
            continue

        tokens = convert_to_tokens(text)
        print(f"[→] Converted: {tokens}")

        path = LEFT_PATH if hemisphere == "left" else RIGHT_PATH
        current_tokens = load_tokens(path)
        current_tokens.extend(tokens)
        save_tokens(path, current_tokens)

        print(f"[+] Tokens added to {hemisphere.upper()} hemisphere. Total now: {len(current_tokens)}\n")

if __name__ == "__main__":
    feed_tokens()
