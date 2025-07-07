# cognitive_anchor_harmonizer.py

import json
from pathlib import Path
from enum import IntEnum

class HueState(IntEnum):
    GRAY = -1
    BLACK = 0
    WHITE = 1

class QbithueNode:
    def __init__(self, token_id, hue_state, resonance, links):
        self.token_id = token_id
        self.hue_state = HueState[hue_state]
        self.resonance = resonance
        self.links = links

    def to_dict(self):
        return {
            "token_id": self.token_id,
            "hue_state": self.hue_state.name,
            "resonance": self.resonance,
            "links": self.links
        }

def load_network(path):
    with open(path, "r") as f:
        data = json.load(f)
    return [QbithueNode(**node) for node in data]

def save_network(path, nodes):
    with open(path, "w") as f:
        json.dump([node.to_dict() for node in nodes], f, indent=2)

def harmonize_anchors(nodes):
    anchor_influence = {}

    # Build frequency count from link references
    for node in nodes:
        for lid in node.links:
            anchor_influence[lid] = anchor_influence.get(lid, 0) + 1

    max_influence = max(anchor_influence.values(), default=1)

    # Reinforce anchor tokens with scaled resonance
    for node in nodes:
        if node.token_id in anchor_influence:
            influence = anchor_influence[node.token_id]
            boost = (influence / max_influence) * 0.5
            node.resonance = min(node.resonance + boost, 1.0)

def main():
    network_path = Path("memory/qbithue_network.json")
    nodes = load_network(network_path)
    harmonize_anchors(nodes)
    save_network(network_path, nodes)
    print("[✓] Cognitive anchor harmonization complete.")

if __name__ == "__main__":
    main()
