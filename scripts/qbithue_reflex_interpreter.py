from pathlib import Path
import json
from enum import Enum
from datetime import datetime

class HueState(Enum):
    GRAY = -1
    BLACK = 0
    WHITE = 1

class QbithueNode:
    def __init__(self, token_id, hue_state, resonance, links):
        self.token_id = token_id
        self.hue_state = HueState[hue_state]
        self.resonance = resonance
        self.links = links

def load_qbithue_network(path="memory/qbithue_network.json"):
    with open(path, "r") as f:
        raw_nodes = json.load(f)
    return [QbithueNode(**node) for node in raw_nodes]

def find_reflex_paths(nodes):
    reflexes = []
    for node in nodes:
        if node.hue_state == HueState.GRAY and node.resonance > 0.0:
            for lid in node.links:
                target = next((n for n in nodes if n.token_id == lid), None)
                if target and target.hue_state == HueState.WHITE and target.resonance > 0.0:
                    reflexes.append({
                        "from": node.token_id,
                        "to": target.token_id,
                        "resonance_out": round(target.resonance, 5)
                    })
    return reflexes

def save_reflex_log(reflexes, path="memory/snapshots/reflex_path_log.json"):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "reflex_arc_count": len(reflexes),
        "reflex_arcs": reflexes
    }

    existing = []
    reflex_log_path = Path(path)
    if reflex_log_path.exists():
        try:
            with reflex_log_path.open("r") as f:
                existing = json.load(f)
        except json.JSONDecodeError:
            existing = []

    existing.append(log_entry)

    with reflex_log_path.open("w") as f:
        json.dump(existing, f, indent=2)

def run_reflex_analysis():
    nodes = load_qbithue_network()
    reflex_paths = find_reflex_paths(nodes)

    if reflex_paths:
        print(f"[⚡] Reflex arcs detected: {len(reflex_paths)}")
        for arc in reflex_paths:
            print(f"    Reflex arc: GRAY {arc['from']} → WHITE {arc['to']} (res {arc['resonance_out']})")
    else:
        print("[…] No reflex arcs triggered.")

    save_reflex_log(reflex_paths)

if __name__ == "__main__":
    run_reflex_analysis()
    