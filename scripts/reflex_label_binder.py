# scripts/reflex_label_binder.py

from memory.label_trait_loader import load_label_trait_map

class ReflexLabelBinder:
    def __init__(self):
        self.trait_map = load_label_trait_map()

    def bind_label(self, label):
        mapping = self.trait_map.get(label)
        if mapping:
            print(f"[BIND] Label '{label}' ➜ Trait: {mapping['trait']}, Reflex: {mapping['reflex_trigger']}, Bias: {mapping['memory_bias']}")
            return mapping
        else:
            print(f"[WARN] Label '{label}' has no trait mapping.")
            return None
