# q_node.py

from tokenizer.q_layer_token import QLayerToken
import random

class QNode:
    def __init__(self, node_type, base_color=None):
        self.node_type = node_type
        self.token = QLayerToken(
            base_color=base_color or self._random_color(),
            fluorescence_tag=[],
            q_state=0,
            field_state={"frequency": 0.0, "amplitude": 0.0},
            mode="propagate"
        )
        self.connected_node = None

    def _random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def connect_node(self, other_node):
        self.connected_node = other_node

    def shift_conscious_state(self, target_state):
        self.token.shift_q_state(target_state)

    def apply_fluorescence(self, tag):
        self.token.add_fluorescence(tag)

    def update_field(self, frequency, amplitude):
        self.token.set_field_state(frequency, amplitude)

    def describe_node(self):
        return {
            "type": self.node_type,
            "token": self.token.describe(),
            "connected_to": self.connected_node.node_type if self.connected_node else None
        }
