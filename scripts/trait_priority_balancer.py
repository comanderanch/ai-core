import json
from pathlib import Path
from datetime import datetime

# File paths
PRIORITY_MAP_PATH = Path("memory/trait_priority_map.json")
OUTPUT_LOG_PATH = Path("memory/trait_priority_balance_log.json")

def load_json(path, fallback):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return fallback
    return fallback

def normalize_priority_scores(priority_scores):
    # Extract all scores
    raw_scores = list(priority_scores.values())
    if not raw_scores:
        return priority_scores  # Nothing to normalize

    max_score = max(raw_scores)
    min_score = min(raw_scores)

    if max_score == min_score:
        return priority_scores  # No variation, nothing to balance

    # Apply min-max normalization
    balanced = {}
    for trait_id, score in priority_scores.items():
        normalized = round((score - min_score) / (max_score - min_score), 4)
        balanced[trait_id] = normalized

    return balanced

def main():
    print("⚖️  Balancing Trait Priorities...")

    data = load_json(PRIORITY_MAP_PATH, {})
    scores = data.get("priority_scores", {})

    if not scores:
        print("[BALANCE] No priority scores found. Balancing skipped.")
        return

    balanced_scores = normalize_priority_scores(scores)

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "balanced_scores": balanced_scores
    }

    with open(OUTPUT_LOG_PATH, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[BALANCE] {len(balanced_scores)} priority scores balanced and saved.")

if __name__ == "__main__":
    main()
