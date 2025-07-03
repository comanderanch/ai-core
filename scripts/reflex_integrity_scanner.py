# scripts/reflex_integrity_scanner.py

import json
from datetime import datetime
from pathlib import Path

# Paths
WEIGHT_LOG = Path("memory/reflex_weight_log.json")
BIAS_LOG = Path("memory/memory_bias_log.json")
RESPONSE_LOG = Path("memory/reflex_response_log.json")
OUTPUT_REPORT = Path("memory/reflex_integrity_report.json")

def load_json(path):
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def scan_integrity():
    weight_map = load_json(WEIGHT_LOG)
    bias_entries = load_json(BIAS_LOG)
    reflex_log = load_json(RESPONSE_LOG)

    bias_map = {entry["label"]: entry["bias"] for entry in bias_entries if "label" in entry and "bias" in entry}

    issues = []

    reflex = reflex_log.get("reflex")
    label = reflex_log.get("label")
    trait = reflex_log.get("trait")

    if reflex not in weight_map:
        issues.append(f"Missing reflex weight for '{reflex}'.")

    if label not in bias_map:
        issues.append(f"Missing memory bias for label '{label}'.")

    if not trait:
        issues.append(f"Missing trait mapping for reflex '{reflex}'.")

    status = "PASS" if not issues else "FAIL"

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "reflex": reflex,
        "label": label,
        "trait": trait,
        "status": status,
        "issues": issues
    }

    with open(OUTPUT_REPORT, "w") as f:
        json.dump(report, f, indent=4)

    print(f"[INTEGRITY] Status: {status}")
    if issues:
        for issue in issues:
            print(f"  - {issue}")

if __name__ == "__main__":
    print("🔍 Running Reflex Integrity Scan...")
    scan_integrity()
