import numpy as np
import json
import random
from pathlib import Path
from datetime import datetime
from enum import IntEnum


# Define hue states
class HueState(IntEnum):
    GRAY = -1  # Emotional buffer / resonance state
    BLACK = 0  # Zero state / memory stasis
    WHITE = 1  # Imaginative trigger / illumination

# Define token resonance node
class QbithueNode:
    def __init__(self, token_id, hue_state: HueState):
        self.token_id = token_id
        self.hue_state = hue_state
        self.resonance = 0.0
        self.links = []

    def update_resonance(self, delta):
        self.resonance += delta
        if self.resonance > 1.0:
            self.resonance = 1.0
        elif self.resonance < -1.0:
            self.resonance = -1.0

    def evaluate_gate(self):
        if self.hue_state == HueState.WHITE:
            return "ignite"
        elif self.hue_state == HueState.GRAY:
            return "reflect"
        elif self.hue_state == HueState.BLACK:
            return "store"
        return "idle"

    def to_dict(self):
        return {
            "token_id": self.token_id,
            "hue_state": self.hue_state.name,
            "resonance": self.resonance,
            "links": self.links
        }

# Generate example network of qbithue nodes
def generate_qbithue_network(token_ids):
    nodes = []
    for token_id in token_ids:
        hue = random.choice(list(HueState))
        node = QbithueNode(token_id, hue)
        node.links = random.sample(token_ids, min(3, len(token_ids)))  # Mock links
        nodes.append(node)
    return nodes

# Save network to file for visualization/debugging
def save_qbithue_network(nodes, path):
    data = [node.to_dict() for node in nodes]
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    # Example: build hue network for tokens 0-19
    token_ids = list(range(20))
    network = generate_qbithue_network(token_ids)
    save_qbithue_network(network, "memory/qbithue_network.json")
    print("[✓] Qbithue Gate Engine initialized with test network.")



