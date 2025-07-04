# scripts/trait_stability_verifier.py

import json
from pathlib import Path
from datetime import datetime

# Paths
MASTER_LOG_PATH = Path("memory/trait_master_log.json")
ANCHOR_LOG_PATH = Path("memory/trait_anchor_stability_log.json")
EQUILIBRIUM_LOG_PATH = Path("memory/trait_equilibrium_log.json")
RESPONSE_LOG_PATH = Path("memory/trait_response_validation_log.json")
OUTPUT_LOG_PATH = Path("memory/trait_stability_verification_log.json")

def load_json(path, fallback=None):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return fallback if fallback is not None else {}
    return fallback if fallback is not None else {}

def verify_trait_stability(master_data, anchor_log, equilibrium_data, response_data):
    anchor_map = {entry["trait_id"]: entry for entry in anchor_log}
    response_map = {entry["trait_id"]: entry for entry in response_data["validated"]}
    results = []

    for trait_id, trait in master_data.get("unified_traits", {}).items():
        bias = trait["bias"]
        weight = trait["weight"]
        drift = trait["influence"]["drift"]

        anchor = anchor_map.get(trait_id, {})
        response = response_map.get(trait_id, {}).get("response", {})
        equilibrium_drift = equilibrium_data.get("summary", {}).get("avg_drift", 0.0)

        is_stable = (
            abs(drift) <= 0.1 and
            anchor.get("state") == "stable" and
            abs(response.get("response_strength", 0.0) - weight) <= 0.2 and
            abs(drift - equilibrium_drift) <= 0.1
        )

        results.append({
            "trait_id": trait_id,
            "bias": bias,
            "weight": weight,
            "drift": drift,
            "anchor_state": anchor.get("state", "unknown"),
            "response_strength": response.get("response_strength", None),
            "equilibrium_drift": equilibrium_drift,
            "status": "stable" if is_stable else "unstable"
        })

    return results

def main():
    print("🔍 Verifying Trait Stability...")

    master_log = load_json(MASTER_LOG_PATH, {})
    anchor_log = load_json(ANCHOR_LOG_PATH, [])
    equilibrium_log = load_json(EQUILIBRIUM_LOG_PATH, {})
    response_log = load_json(RESPONSE_LOG_PATH, {})

    if not master_log or not anchor_log or not equilibrium_log or not response_log:
        print("[VERIFY] Missing required data. Verification skipped.")
        return

    summary = verify_trait_stability(master_log, anchor_log, equilibrium_log, response_log)

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "verification": summary
    }

    with open(OUTPUT_LOG_PATH, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[VERIFY] Stability verification complete. {len(summary)} traits checked.")

if __name__ == "__main__":
    main()
