import json
import os
from datetime import datetime

PRINCIPLE_SOURCE = "memory/core_guiding_principles.json"
OUTPUT_PATH = "memory/injected_principles_log.json"

def load_principles():
    if not os.path.exists(PRINCIPLE_SOURCE):
        print("[PrincipleInjector] No core principle file found.")
        return []

    with open(PRINCIPLE_SOURCE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("[PrincipleInjector] Malformed JSON in core principles.")
            return []

def inject_principles(principles):
    injected = []

    for principle in principles:
        injected.append({
            "name": principle.get("name"),
            "description": principle.get("description"),
            "guides": principle.get("guides", []),  # e.g. actions, tones, tokens
            "weight": principle.get("weight", 1.0),
            "injected_at": datetime.utcnow().isoformat() + "Z"
        })

    with open(OUTPUT_PATH, "w") as f:
        json.dump(injected, f, indent=4)

    print(f"[PrincipleInjector] Injected {len(injected)} guiding principles.")
    print(f"[PrincipleInjector] Log saved to {OUTPUT_PATH}")

def run_principle_injection():
    print("[PrincipleInjector] Injecting core guidance into system memory...")
    principles = load_principles()
    if not principles:
        print("[PrincipleInjector] No principles injected.")
        return

    inject_principles(principles)
    print("[PrincipleInjector] Injection complete.")

if __name__ == "__main__":
    run_principle_injection()
