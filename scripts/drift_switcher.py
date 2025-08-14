# drift_switcher.py
# Phase 38.3 – Automatically switches active hemisphere on output drift

from hemisphere_manager import HemisphereManager
from llm_output_resolver import LLMOutputResolver
from datetime import datetime
import json
from pathlib import Path

class DriftSwitcher:
    def __init__(self):
        self.hm = HemisphereManager()
        self.resolver = LLMOutputResolver()
        self.log_path = Path("memory/snapshots/drift_switch_log.json")

    def run_check(self):
        result = self.resolver.resolve_outputs()

        log_entry = {
            "timestamp": result["timestamp"],
            "active_hemisphere": result["active_hemisphere"],
            "drift_detected": result["drift_detected"],
            "switched": False,
            "new_active_hemisphere": result["active_hemisphere"]
        }

        if result["drift_detected"]:
            self.hm.switch_hemisphere()
            log_entry["switched"] = True
            log_entry["new_active_hemisphere"] = self.hm.get_current_hemisphere()

        self._append_log(log_entry)

        if log_entry["switched"]:
            print(f"[↺] Drift detected. Hemisphere switched to {log_entry['new_active_hemisphere'].upper()}.")
        else:
            print(f"[✓] No drift. Staying on {log_entry['active_hemisphere'].upper()}.")

    def _append_log(self, entry):
        log = []
        if self.log_path.exists():
            try:
                with self.log_path.open("r") as f:
                    log = json.load(f)
            except json.JSONDecodeError:
                log = []

        log.append(entry)

        with self.log_path.open("w") as f:
            json.dump(log, f, indent=2)

if __name__ == "__main__":
    switcher = DriftSwitcher()
    switcher.run_check()
