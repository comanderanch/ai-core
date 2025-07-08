# em_field_balancer.py

import random

class ElectromagneticField:
    def __init__(self, field_strength=1000):
        self.field_strength = field_strength
        self.internal_fluctuation = 0
        self.external_resistance = 0

    def detect_fluctuations(self):
        self.internal_fluctuation = random.uniform(-10, 10)
        return self.internal_fluctuation

    def detect_resistance(self):
        self.external_resistance = random.uniform(0, 15)
        return self.external_resistance

    def balance_field(self):
        total_imbalance = self.internal_fluctuation + self.external_resistance
        if total_imbalance > 0:
            kinetic_energy = total_imbalance * 1.5
            self.field_strength -= kinetic_energy
            return kinetic_energy
        return 0  # No balancing needed

    def apply_force(self):
        force_needed = random.uniform(5, 20)
        if self.field_strength >= force_needed:
            self.field_strength -= force_needed
            return force_needed
        return None  # Not enough strength

    def report(self):
        return {
            "field_strength": self.field_strength,
            "internal_fluctuation": self.internal_fluctuation,
            "external_resistance": self.external_resistance
        }
