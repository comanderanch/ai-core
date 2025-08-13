# scripts/thread_bind_converter.py
import json
from pathlib import Path
from datetime import datetime

LEGACY_PATH = Path("memory/thread_binds/legacy_thread_binds.json")
BIND_MAP_PATH = Path("memory/thread_binds/bind_map.json")

def convert_legacy_to_bind_map():
    if not LEGACY_PATH.exists():
        print(f"[ERROR] Missing: {LEGACY_PATH}")
        return

    with open(LEGACY_PATH, "r") as f:
        legacy_data = json.load(f)

    binds = legacy_data.get("thread_binds", [])
    bind_map = {}

    for bind in binds:
        token = bind.get("mapped_token")
        if token not in bind_map:
            bind_map[token] = {
                "path": [],
                "origin": bind.get("origin", "unknown"),
                "type": bind.get("type", "unspecified"),
                "frequency": bind.get("frequency", 0),
                "bound_at": bind.get("bound_at", datetime.utcnow().isoformat())
            }
        bind_map[token]["path"].append(bind.get("origin"))

    with open(BIND_MAP_PATH, "w") as f:
        json.dump(bind_map, f, indent=2)

    print(f"[Converter] Converted legacy thread binds → bind_map.json ({len(bind_map)} tokens)")

if __name__ == "__main__":
    convert_legacy_to_bind_map()


