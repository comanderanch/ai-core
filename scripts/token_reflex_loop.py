import json
from collections import Counter, defaultdict
import os

TRAIL_LOG_PATH = "../memory/token_trail_log.json"
REFLEX_LOG_PATH = "../memory/reflex_tokens_log.json"  # New log file to track reflex tokens
THRESHOLD = 2  # Lowered threshold to detect tokens repeating twice

def load_token_log(path=TRAIL_LOG_PATH):
    if not os.path.exists(path):
        print(f"❌ Token trail log not found at {path}")
        return []
    with open(path, "r") as f:
        return json.load(f)

def detect_token_loops(log, threshold=THRESHOLD):
    counter = Counter(entry["input_index"] for entry in log)
    return {token: count for token, count in counter.items() if count >= threshold}

def analyze_patterns(log, loop_tokens):
    patterns = defaultdict(list)
    for entry in log:
        idx = entry["input_index"]
        if idx in loop_tokens:
            patterns[idx].append(entry["output_summary"]["mean"])
    return patterns

def log_reflex_tokens(reflex_tokens):
    # Ensure the directory exists first
    log_dir = os.path.dirname(REFLEX_LOG_PATH)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Write to the log file (create if it doesn't exist)
    with open(REFLEX_LOG_PATH, "a") as f:
        json.dump(reflex_tokens, f, indent=4)
        f.write("\n")  # Newline to separate each entry for easier reading

def main():
    log = load_token_log()
    if not log:
        return

    print(f"📜 Loaded {len(log)} token log entries.")

    loop_tokens = detect_token_loops(log)
    if not loop_tokens:
        print("⚠️ No repeating token patterns detected.")
        return

    print("🔁 Reflex-triggering tokens:")
    reflex_tokens = []
    for token, count in loop_tokens.items():
        print(f"  Token {token} → seen {count} times")
        reflex_tokens.append({"token": token, "count": count})

    # Log reflex tokens to file
    log_reflex_tokens(reflex_tokens)

    patterns = analyze_patterns(log, loop_tokens)
    print("\n📊 Mean output summaries for reflex tokens:")
    for token, means in patterns.items():
        print(f"  Token {token} → Means: {means}")

if __name__ == "__main__":
    main()
