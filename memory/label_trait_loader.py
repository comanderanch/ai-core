# memory/label_trait_loader.py

import json
import os

LABEL_TRAIT_FILE = os.path.join(os.path.dirname(__file__), "label_trait_map.json")

def load_label_trait_map():
    try:
        with open(LABEL_TRAIT_FILE, "r") as file:
            data = json.load(file)
            print(f"[LOAD] Loaded {len(data)} label-trait mappings.")
            return data
    except FileNotFoundError:
        print(f"[ERROR] '{LABEL_TRAIT_FILE}' not found.")
        return {}
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse label_trait_map.json: {e}")
        return {}
