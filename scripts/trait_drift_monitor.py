import json
from pathlib import Path
from datetime import datetime

# File paths
memory_log_path = Path("memory/trait_memory_log.json")
drift_log_path = Path("memory/trait_drift_log.json")

# Load trait memory log
with open(memory_log_path, "r") as f:
    memory_log = json.load(f)

# Get ordered phases
history = memory_log.get("history", [])
if len(history) < 2:
    print("[✗] Not enough history to detect drift.")
    exit(1)

# Compare last and previous phase
latest = history[-1]
previous = history[-2]

latest_traits = latest["traits"]
previous_traits = previous["traits"]

# Calculate drift
drift_report = {
    "timestamp": datetime.utcnow().isoformat(),
    "phase_from": previous["phase"],
    "phase_to": latest["phase"],
    "weight_drift": abs(latest_traits["final_loss"] - previous_traits["final_loss"]),
    "details": {
        "previous_loss": previous_traits["final_loss"],
        "current_loss": latest_traits["final_loss"]
    }
}

# Load or create drift log
if drift_log_path.exists():
    with open(drift_log_path, "r") as f:
        drift_data = json.load(f)
else:
    drift_data = []

drift_data.append(drift_report)

# Save updated drift log
with open(drift_log_path, "w") as f:
    json.dump(drift_data, f, indent=2)

print(f"[✓] Drift logged between {previous['phase']} and {latest['phase']}.")
