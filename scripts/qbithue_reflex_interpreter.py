from pathlib import Path
import json
from pathlib import Path
from enum import Enum

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
                    reflexes.append((node.token_id, target.token_id))
    return reflexes

def run_reflex_analysis():
    nodes = load_qbithue_network()
    reflex_paths = find_reflex_paths(nodes)

    if reflex_paths:
        print(f"[⚡] Reflex arcs detected: {len(reflex_paths)}")
        for src, dst in reflex_paths:
            print(f"    Reflex arc: GRAY {src} → WHITE {dst}")
    else:
        print("[…] No reflex arcs triggered.")

if __name__ == "__main__":
    run_reflex_analysis()


# Write to scripts/
Path("scripts").mkdir(exist_ok=True)
path = Path("scripts/qbithue_reflex_interpreter.py")
#path.write_text(qbithue_reflex_interpreter.strip())
