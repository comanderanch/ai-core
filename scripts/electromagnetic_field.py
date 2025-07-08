import os
import random
import time

class ElectromagneticField:
    def __init__(self, field_strength):
        self.field_strength = field_strength
        self.internal_fluctuation = 0
        self.external_resistance = 0

    def detect_fluctuations(self):
        self.internal_fluctuation = random.uniform(-10, 10)
        print(f"[Step 1] Internal Fluctuation: {self.internal_fluctuation:.2f}")

    def detect_resistance(self):
        self.external_resistance = random.uniform(0, 15)
        print(f"[Step 2] External Resistance: {self.external_resistance:.2f}")

    def balance_field(self):
        total_imbalance = self.internal_fluctuation + self.external_resistance
        kinetic_energy = total_imbalance * 1.5
        print(f"[Step 3] Applied {kinetic_energy:.2f} units of kinetic energy to stabilize.")
        self.field_strength -= kinetic_energy

    def apply_force(self):
        force_needed = random.uniform(5, 20)
        print(f"[Step 4] Applied {force_needed:.2f} units of field force.")
        self.field_strength -= force_needed

    def report(self):
        print(f"\\n[Final State]\\nfield_strength: {self.field_strength:.2f}\\n"
              f"internal_fluctuation: {self.internal_fluctuation:.2f}\\n"
              f"external_resistance: {self.external_resistance:.2f}\\n")

if __name__ == "__main__":
    field_strength = int(os.getenv("FIELD_STRENGTH", 1000))
    field = ElectromagneticField(field_strength)
    field.detect_fluctuations()
    field.detect_resistance()
    field.balance_field()
    field.apply_force()
    field.report()