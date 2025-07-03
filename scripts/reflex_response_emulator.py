# scripts/reflex_response_emulator.py

import json
import os

LABEL_MAP_PATH = "memory/label_trait_map.json"
FEEDBACK_LOG_PATH = "memory/reflex_feedback_log.json"

class ReflexResponseEmulator:
    def __init__(self):
        self.label_map = self._load_label_map()

    def _load_label_map(self):
        if not os.path.exists(LABEL_MAP_PATH):
            print(f"[ERROR] Missing label map: {LABEL_MAP_PATH}")
            return {}
        with open(LABEL_MAP_PATH, "r") as f:
            return json.load(f)

    def trigger_reflex(self, label):
        if label not in self.label_map:
            print(f"[WARN] Label '{label}' not found in label map.")
            return

        reflex = self.label_map[label]["reflex_trigger"]
        trait = self.label_map[label]["trait"]
        bias = self.label_map[label]["memory_bias"]

        print(f"[REFLEX] Label '{label}' ➜ Reflex: '{reflex}' | Trait: '{trait}' | Bias: {bias}")
        self._log_feedback(label, reflex, trait, bias)

    def _log_feedback(self, label, reflex, trait, bias):
        log_entry = {
            "label": label,
            "reflex_trigger": reflex,
            "trait": trait,
            "bias": bias
        }

        try:
            if os.path.exists(FEEDBACK_LOG_PATH):
                with open(FEEDBACK_LOG_PATH, "r") as f:
                    log = json.load(f)
            else:
                log = []

            log.append(log_entry)

            with open(FEEDBACK_LOG_PATH, "w") as f:
                json.dump(log, f, indent=2)
            print(f"[LOG] Reflex feedback logged.")
        except Exception as e:
            print(f"[ERROR] Failed to log reflex feedback: {e}")
