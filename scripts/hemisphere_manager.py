# hemisphere_manager.py
# Phase 38.1 – Manages left/right hemisphere token sets for AI-Core

import json
from pathlib import Path

class HemisphereManager:
    def __init__(self,
                 left_path=Path("tokenizer/token_set_left.json"),
                 right_path=Path("tokenizer/token_set_right.json")):

        self.paths = {"left": left_path, "right": right_path}
        self.active = "left"

        self.token_sets = {
            "left": self._load_tokens(left_path),
            "right": self._load_tokens(right_path)
        }

    def _load_tokens(self, path: Path):
        # Ensure file exists and is a JSON array
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("[]", encoding="utf-8")
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
            # Coerce non-list to list to avoid crashes
            return list(data)
        except Exception:
            # Corrupt or empty: reset to empty list
            return []

    def _save_tokens(self, hemisphere: str):
        path = self.paths[hemisphere]
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(self.token_sets[hemisphere], f, ensure_ascii=False)

    def get_active_tokens(self):
        return self.token_sets[self.active]

    def switch_hemisphere(self):
        self.active = "right" if self.active == "left" else "left"
        print(f"[⇄] Hemisphere switched. Now using: {self.active.upper()}")

    def get_current_hemisphere(self):
        return self.active

    def get_all_tokens(self):
        return {
            "left": self.token_sets["left"],
            "right": self.token_sets["right"]
        }

    def add_tokens(self, hemisphere: str, tokens: list):
        """
        Append tokens to the selected hemisphere AND persist to disk
        so token_size_reporter sees growth.
        """
        if hemisphere not in self.token_sets:
            self.token_sets[hemisphere] = []
        self.token_sets[hemisphere].extend(tokens)
        self._save_tokens(hemisphere)

    # Optional: tiny helper for debugging
    def size(self, hemi: str):
        return len(self.token_sets.get(hemi, []))


if __name__ == "__main__":
    manager = HemisphereManager()
    print(f"[🧠] Active hemisphere: {manager.get_current_hemisphere()}")
    print("[🔡] Token sample:", manager.get_active_tokens()[:5])
