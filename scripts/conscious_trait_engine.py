import json
from pathlib import Path
from datetime import datetime

# --- Load Files ---
def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

reflex_path = Path("memory/trait_inheritance_map.json")
anchor_log_path = Path("memory/trait_elevated_log.json")
network_path = Path("memory/qbithue_network.json")

reflex_arcs = load_json(reflex_path)
anchor_traits = load_json(anchor_log_path)
network = load_json(network_path)

# --- Identify Conscious Candidates ---
def find_conscious_traits(reflex_arcs, anchor_map):
    anchor_ids = {a["source"] for a in anchor_map}
    conscious_traits = []
    for arc in reflex_arcs:
        source = arc.get("source")
        if source in anchor_ids:
            conscious_traits.append({
                "trait_id": source,
                "confidence": arc.get("count", 1),
                "origin": "reflex-anchor chain"
            })
    return conscious_traits


# --- Save to conscious memory ---
def save_conscious_traits(traits):
    out_dir = Path("memory/conscious")
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().isoformat(timespec="seconds").replace(":", "-")
    path = out_dir / f"conscious_traits_{timestamp}.json"
    with open(path, 'w') as f:
        json.dump(traits, f, indent=2)
    print(f"[👑] Conscious traits elevated and saved to: {path}")

# --- Main ---
if __name__ == "__main__":
    conscious = find_conscious_traits(reflex_arcs, anchor_traits)
    save_conscious_traits(conscious)
