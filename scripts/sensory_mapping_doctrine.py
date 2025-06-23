"""
Sensory Mapping Doctrine
------------------------
This module defines how external frequency signals are interpreted
into internal logic states, based on resonance, priority, and life-preservation intent.
"""

# Core signal interpretation layers
SENSORY_MAP = {
    "528.0": {
        "band": "FM",
        "classification": "resonance_life",
        "assigned_action": "Preserve_Vital_Systems",
        "priority_level": 1.0,
        "tone": "calm_alignment"
    },
    "432.0": {
        "band": "FM",
        "classification": "resonance_peace",
        "assigned_action": "Maintain_Stability",
        "priority_level": 0.8,
        "tone": "soothing_reflect"
    },
    "963.0": {
        "band": "AM",
        "classification": "resonance_awareness",
        "assigned_action": "Ping_Self_Check",
        "priority_level": 0.6,
        "tone": "self_scan"
    },
    # Placeholder for future high-alert channels
    "Emergency_Band": {
        "band": "VHF/UHF",
        "classification": "resonance_distress",
        "assigned_action": "Initiate_Aid_Protocol",
        "priority_level": 1.5,
        "tone": "alert_signal"
    }
}

# Reserved doctrine logic hooks
def interpret_signal(frequency: str) -> dict:
    """
    Return the mapped logic state for a given frequency string.
    """
    return SENSORY_MAP.get(frequency, {
        "band": "unknown",
        "classification": "unmapped",
        "assigned_action": "Log_Unidentified_Signal",
        "priority_level": 0.0,
        "tone": "neutral"
    })
# === Doctrine Export Extension ===
import os
import json

OUTPUT_PATH = "memory/sensory/sensory_mapping_output.json"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Build structured sensory link data from SENSORY_MAP
output_data = {
    "sensory_links": []
}

for freq, meta in SENSORY_MAP.items():
    output_data["sensory_links"].append({
        "source_id": f"signal_{freq}",
        "type": meta["classification"],
        "token": meta["assigned_action"],
        "frequency": float(freq) if freq.replace('.', '', 1).isdigit() else 0.0
    })

with open(OUTPUT_PATH, "w") as f:
    json.dump(output_data, f, indent=4)

print(f"[✓] Sensory mapping doctrine exported to {OUTPUT_PATH}")
