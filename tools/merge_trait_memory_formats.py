import json
from pathlib import Path
from datetime import datetime

# Paths
legacy_path = Path("memory/trait_memory_log.json")

# Backup original
backup_path = legacy_path.with_name("trait_memory_log_backup.json")
if not backup_path.exists():
    legacy_path.rename(backup_path)

# Load legacy list
with open(backup_path, "r") as f:
    try:
        legacy_list = json.load(f)
        assert isinstance(legacy_list, list)
    except Exception as e:
        print(f"[✗] Failed to load legacy trait list: {e}")
        exit(1)

# Build merged format
merged_format = {
    "legacy_traits": legacy_list,
    "linked_phases": [],
    "trait_evolution": {},
    "history": []
}

# Save updated format
with open(legacy_path, "w") as f:
    json.dump(merged_format, f, indent=2)

print("[✓] Trait memory log upgraded to dual-format.")
print(f"[✓] Legacy data preserved under: {backup_path}")
