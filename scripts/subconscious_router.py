from pathlib import Path
import json
from enum import Enum
from pathlib import Path

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

    def route_resonance(self, network):
        if self.hue_state == HueState.GRAY and self.resonance > 0.0:
            for lid in self.links:
                target = next((n for n in network if n.token_id == lid), None)
                if target and target.hue_state != HueState.BLACK:
                    delta = 0.01
                    target.resonance += delta
                    self.resonance -= delta / 2
                    print(f"[↗] Routed 0.01 resonance: GRAY {self.token_id} → {target.hue_state.name} {target.token_id}")

def load_network(path):
    with open(path) as f:
        data = json.load(f)
    return [QbithueNode(n["token_id"], n["hue_state"], n["resonance"], n["links"]) for n in data]

def save_network(path, nodes):
    data = [
        {
            "token_id": n.token_id,
            "hue_state": n.hue_state.name,
            "resonance": round(n.resonance, 5),
            "links": n.links
        }
        for n in nodes
    ]
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# Execute
network_path = Path("memory/qbithue_network.json")
network = load_network(network_path)

for node in network:
    node.route_resonance(network)

save_network(network_path, network)
print("[✓] Subconscious routing complete and saved.")

