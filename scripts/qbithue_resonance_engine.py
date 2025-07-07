import json
import random
from enum import IntEnum
from pathlib import Path

# === Load the Qbithue Node Definition ===
class HueState(IntEnum):
    BLACK = 0     # resistance / block
    GRAY = -1     # reflex / relay
    WHITE = 1     # anchor / signal

class QbithueNode:
    def __init__(self, token_id, hue_state, links):
        self.token_id = token_id
        self.hue_state = HueState[hue_state]
        self.resonance = 0.0
        self.links = links

    def propagate_resonance(self, amount):
        if self.hue_state == HueState.BLACK:
            return []  # blocks signal
        self.resonance += amount
        return self.links if self.hue_state == HueState.GRAY else []

# === Load Existing Network ===
network_path = Path("memory/qbithue_network.json")
if not network_path.exists():
    raise FileNotFoundError("Qbithue network not found at memory/qbithue_network.json")

with network_path.open("r") as f:
    raw_nodes = json.load(f)

node_map = {node["token_id"]: QbithueNode(node["token_id"], node["hue_state"], node["links"]) for node in raw_nodes}

# === Resonance Propagation ===
def run_resonance_pulse(seed_id, strength=1.0, decay=0.2, max_depth=5):
    visited = set()
    queue = [(seed_id, strength, 0)]

    while queue:
        node_id, current_strength, depth = queue.pop(0)
        if node_id in visited or current_strength <= 0 or depth > max_depth:
            continue

        visited.add(node_id)
        node = node_map[node_id]
        linked_ids = node.propagate_resonance(current_strength)

        for linked_id in linked_ids:
            if linked_id not in visited:
                queue.append((linked_id, current_strength - decay, depth + 1))

# === Run Pulse from a White Node ===
white_nodes = [n for n in node_map.values() if n.hue_state == HueState.WHITE]
if white_nodes:
    seed = random.choice(white_nodes)
    print(f"[⚡] Starting resonance pulse from token {seed.token_id} (WHITE)")
    run_resonance_pulse(seed.token_id)

# === Save Updated Network State ===
updated_nodes = []
for node in node_map.values():
    updated_nodes.append({
        "token_id": node.token_id,
        "hue_state": node.hue_state.name,
        "resonance": round(node.resonance, 5),
        "links": node.links
    })

Path("memory/qbithue_network.json").write_text(json.dumps(updated_nodes, indent=2))
print("[✓] Resonance propagation complete and saved.")
