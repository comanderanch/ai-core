import json
from pathlib import Path
from datetime import datetime

# Paths
output_log_path = Path("training/training_output_log.json")
trait_memory_log_path = Path("memory/trait_memory_log.json")

# Load training log
with open(output_log_path, "r") as f:
    training_log = json.load(f)

# Extract phases
phases = training_log.get("output_summary", {}).get("phases", {})
if not isinstance(phases, dict) or not phases:
    print("[✗] No valid phase data found in training log.")
    exit(1)

# Load or initialize trait memory log
if trait_memory_log_path.exists():
    with open(trait_memory_log_path, "r") as f:
        memory_log = json.load(f)
else:
    memory_log = {
        "linked_phases": [],
        "trait_evolution": {},
        "history": []
    }

# Append new trait links
for phase_name, phase_data in phases.items():
    if phase_name in memory_log.get("linked_phases", []):
        continue  # Already recorded

    traits = {
        "sample_count": phase_data.get("sample_count", 0),
        "epochs": phase_data.get("epochs", 0),
        "final_loss": phase_data.get("final_loss", None)
    }

    memory_log["linked_phases"].append(phase_name)
    memory_log["trait_evolution"][phase_name] = traits
    memory_log["history"].append({
        "phase": phase_name,
        "timestamp": datetime.utcnow().isoformat(),
        "traits": traits
    })

# Save updated log
with open(trait_memory_log_path, "w") as f:
    json.dump(memory_log, f, indent=2)

print("[✓] Trait memory linked successfully.")
