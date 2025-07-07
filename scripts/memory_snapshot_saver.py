import json
from pathlib import Path
from datetime import datetime

# Path to the current network file
network_path = Path("memory/qbithue_network.json")

# Directory to store snapshots
snapshot_dir = Path("memory/snapshots/")
snapshot_dir.mkdir(parents=True, exist_ok=True)

# Load the current network
with network_path.open("r") as file:
    network_data = json.load(file)

# Format timestamp for filename
timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
snapshot_path = snapshot_dir / f"qbithue_snapshot_{timestamp}.json"

# Save the snapshot
with snapshot_path.open("w") as file:
    json.dump(network_data, file, indent=2)

print(f"[✓] Snapshot saved to {snapshot_path}")
