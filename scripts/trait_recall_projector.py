import json
from pathlib import Path
from datetime import datetime

# === File Paths ===
log_path = Path("memory/trait_memory_log.json")
output_path = Path("logs/trait_recall_projection.json")

# === Load Memory Log ===
if not log_path.exists():
    print("[✗] Trait memory log not found.")
    exit(1)

with open(log_path, "r") as f:
    memory_data = json.load(f)

# === Extract History ===
history = memory_data.get("history", [])
if not history:
    print("[✗] No historical trait data found.")
    exit(1)

# === Build Recall Projection ===
recall_projection = {
    "timestamp": datetime.utcnow().isoformat(),
    "recall_summary": []
}

for entry in history:
    phase = entry.get("phase")
    traits = entry.get("traits", {})
    
    projection = {
        "phase": phase,
        "sample_count": traits.get("sample_count"),
        "epochs": traits.get("epochs"),
        "final_loss": traits.get("final_loss"),
        "retention_score": round(1 / (traits.get("final_loss", 1) + 1e-6), 4)
    }

    recall_projection["recall_summary"].append(projection)

# === Save Projection Log ===
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w") as f:
    json.dump(recall_projection, f, indent=2)

print(f"[✓] Trait recall projection completed: {output_path}")
