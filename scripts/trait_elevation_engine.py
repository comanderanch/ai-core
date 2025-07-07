import json
from collections import Counter
from pathlib import Path

SNAPSHOT_DIR = Path("memory/snapshots")
TRAIT_OUTPUT_PATH = Path("memory/elevated_traits.json")

# Find the most recent snapshot file
def get_latest_snapshot():
    snapshots = sorted(SNAPSHOT_DIR.glob("qbithue_snapshot_*.json"), reverse=True)
    if not snapshots:
        raise FileNotFoundError("No snapshot files found.")
    return snapshots[0]

# Load snapshot data
def load_snapshot(path):
    with open(path, "r") as f:
        return json.load(f)

# Detect strong reflex arcs
def detect_reflex_arcs(nodes):
    arcs = []
    for node in nodes:
        if node["hue_state"] == "GRAY" and node["resonance"] > 0.0:
            for lid in node["links"]:
                target = next((n for n in nodes if n["token_id"] == lid), None)
                if target and target["hue_state"] == "WHITE" and target["resonance"] > 0.0:
                    arcs.append((node["token_id"], target["token_id"]))
    return arcs

# Elevate frequently triggered arcs to traits
def elevate_traits(arcs, threshold=1):
    counts = Counter(arcs)
    elevated = [{"source": a[0], "target": a[1], "count": c}
                for a, c in counts.items() if c >= threshold]
    return elevated

# Save promoted traits
def save_traits(traits):
    TRAIT_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TRAIT_OUTPUT_PATH, "w") as f:
        json.dump(traits, f, indent=2)

# --- Main Execution ---
if __name__ == "__main__":
    try:
        snapshot_file = get_latest_snapshot()
        data = load_snapshot(snapshot_file)
        reflex_arcs = detect_reflex_arcs(data)
        elevated = elevate_traits(reflex_arcs, threshold=1)

        # Save elevated traits to log for linking
        with open("memory/trait_elevated_log.json", "w") as f:
            json.dump(elevated, f, indent=2)

        print(f"[✓] Trait elevation complete. {len(elevated)} traits promoted and saved.")
    except Exception as e:
        print(f"[!] Error during trait elevation: {e}")

