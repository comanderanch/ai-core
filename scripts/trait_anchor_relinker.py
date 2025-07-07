# trait_anchor_relinker.py
import json
from pathlib import Path
from enum import Enum


class HueState(Enum):
    BLACK = -1
    GRAY = 0
    WHITE = 1


class QbithueNode:
    def __init__(self, token_id, hue_state, resonance, links):
        self.token_id = token_id
        self.hue_state = HueState[hue_state]
        self.resonance = resonance
        self.links = links


def load_network(path):
    with open(path) as f:
        data = json.load(f)
    return [QbithueNode(n["token_id"], n["hue_state"], n["resonance"], n["links"]) for n in data]


def load_traits(path):
    if not path.exists():
        return []
    with path.open() as f:
        return json.load(f)


def find_new_inheritance_links(nodes, elevated_traits):
    new_links = []
    elevated_ids = {t["source"] for t in elevated_traits} | {t["target"] for t in elevated_traits}

    for node in nodes:
        if node.token_id in elevated_ids and node.resonance > 0.0:
            for lid in node.links:
                target = next((n for n in nodes if n.token_id == lid), None)
                if target and target.hue_state == HueState.GRAY and target.resonance > 0.0:
                    new_links.append({
                        "from": node.token_id,
                        "to": target.token_id,
                        "type": "anchor-relink"
                    })
    return new_links


# Paths
network_path = Path("memory/qbithue_network.json")
traits_path = Path("memory/elevated_traits.json")
inherit_path = Path("memory/trait_inheritance_map.json")

# Load data
network = load_network(network_path)
elevated_traits = load_traits(traits_path)
existing_links = load_traits(inherit_path)

# Find and merge
new_links = find_new_inheritance_links(network, elevated_traits)
merged_links = existing_links + new_links

# Save
with inherit_path.open("w") as f:
    json.dump(merged_links, f, indent=2)

print(f"[✓] Trait anchor relinking complete. {len(new_links)} new paths added.")
