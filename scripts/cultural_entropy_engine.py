# scripts/cultural_entropy_engine.py

"""
Cultural Entropy Engine
Evaluates resonance variability and stability drift across the Qbithue network
to simulate entropy-based memory evolution and cultural drift.
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Load network
def load_network(path):
    with open(path, 'r') as f:
        return json.load(f)

# Save updated network
def save_network(path, network):
    with open(path, 'w') as f:
        json.dump(network, f, indent=2)

# Evaluate entropy
def apply_entropy_drift(network):
    for node in network:
        if node["hue_state"] == "GRAY":
            drift = 0.1
        elif node["hue_state"] == "WHITE":
            drift = -0.05
        else:  # BLACK
            drift = 0.0
        node["resonance"] = max(0.0, min(1.0, node["resonance"] + drift))
    return network

# Snapshot result
def snapshot_entropy(network):
    ts = datetime.now().isoformat().replace(":", "-").split(".")[0]
    out_dir = Path("memory/entropy_snapshots")
    out_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = out_dir / f"entropy_snapshot_{ts}.json"
    with open(snapshot_path, "w") as f:
        json.dump(network, f, indent=2)
    return snapshot_path

# Main execution
if __name__ == "__main__":
    path = "memory/qbithue_network.json"
    if not os.path.exists(path):
        print("[!] Qbithue network not found.")
    else:
        network = load_network(path)
        network = apply_entropy_drift(network)
        save_network(path, network)
        snapshot_file = snapshot_entropy(network)
        print(f"[🌐] Cultural entropy applied and saved to: {snapshot_file}")
