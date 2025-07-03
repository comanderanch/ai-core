import json
from collections import defaultdict
from pathlib import Path

LOG_PATH = Path("memory/reflex_response_log.json")
AGG_PATH = Path("memory/reflex_influence_summary.json")

def load_log():
    if not LOG_PATH.exists():
        print("[WARN] No reflex log found.")
        return []
    with open(LOG_PATH, 'r') as f:
        return [json.loads(line) for line in f if line.strip()]

def aggregate(logs):
    count_map = defaultdict(int)
    for entry in logs:
        reflex = entry.get("reflex")
        if reflex:
            count_map[reflex] += 1
    return dict(count_map)

def save_summary(summary):
    with open(AGG_PATH, 'w') as f:
        json.dump(summary, f, indent=4)
    print(f"[SAVE] Reflex influence summary saved to {AGG_PATH}")

if __name__ == "__main__":
    logs = load_log()
    summary = aggregate(logs)
    save_summary(summary)
