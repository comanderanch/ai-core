# scripts/conscious_path_resolver.py

import json
from pathlib import Path
from datetime import datetime

SNAPSHOT_PATH = Path("memory/snapshots/qbithue_state_log.json")
THREAD_BINDS_PATH = Path("memory/thread_binds/bind_map.json")
OUTPUT_PATH = Path("memory/conscious/active_pathways.json")

def load_json(path):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def resolve_paths(qbithue_data, bind_map):
    resolved = []
    for token, details in bind_map.items():
        state = qbithue_data.get(token, {})
        q_state = state.get("q_state", 0)
        resonance = state.get("resonance", 0.0)
        resilience = resonance 
        # Elevation criteria: strong positive Q-state or resonance peak
        if q_state == 1 and resilience >= 0.5:
            resolved.append({
                "token": token,
                "path": details.get("path", []),
                "q_state": q_state,
                "resilience": resilience,
                "timestamp": datetime.utcnow().isoformat()
            })

    return resolved

def save_paths(data):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)

def main():
    qbithue_data = load_json(SNAPSHOT_PATH)
    bind_map = load_json(THREAD_BINDS_PATH)
    resolved = resolve_paths(qbithue_data, bind_map)
    save_paths(resolved)

    print(f"[Resolver] Resolved {len(resolved)} active conscious pathways.")
    if resolved:
        print("  Sample:", resolved[0])

if __name__ == "__main__":
    main()
