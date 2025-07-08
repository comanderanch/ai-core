# q_layer_token.py

import random

class QLayerToken:
    def __init__(self, base_color, fluorescence_tag=None, q_state=0, field_state=None, mode="propagate"):
        """
        Initializes a Q-layer token for cognitive resonance and routing.

        :param base_color: RGB tuple representing the token’s base identity
        :param fluorescence_tag: String or list defining token behavior (e.g., 'memory', 'logic')
        :param q_state: Qbithue state: -1 (gray), 0 (black/static), +1 (white/conscious)
        :param field_state: Dict containing frequency and amplitude
        :param mode: Token mode – 'propagate', 'collapse', or 'echo'
        """
        self.base_color = base_color
        self.fluorescence_tag = fluorescence_tag or []
        self.q_state = q_state
        self.field_state = field_state or {"frequency": 0.0, "amplitude": 0.0}
        self.mode = mode

    def set_field_state(self, frequency, amplitude):
        self.field_state["frequency"] = frequency
        self.field_state["amplitude"] = amplitude

    def shift_q_state(self, new_state):
        assert new_state in [-1, 0, 1], "Invalid Q-state."
        self.q_state = new_state

    def add_fluorescence(self, tag):
        if tag not in self.fluorescence_tag:
            self.fluorescence_tag.append(tag)

    def clear_fluorescence(self):
        self.fluorescence_tag = []

    def describe(self):
        return {
            "color": self.base_color,
            "fluorescence": self.fluorescence_tag,
            "q_state": self.q_state,
            "field": self.field_state,
            "mode": self.mode
        }
