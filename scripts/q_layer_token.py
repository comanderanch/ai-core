# q_layer_token.py

from tokenizer.q_layer_token import QLayerToken
import random

def generate_q_token(base_color=None, tag_list=None, mode="propagate"):
    """
    Create a Q-layer token with optional color, tags, and behavior mode.
    """
    token = QLayerToken(
        base_color=base_color or random_color(),
        fluorescence_tag=tag_list or [],
        q_state=0,
        field_state={"frequency": 0.0, "amplitude": 0.0},
        mode=mode
    )
    return token

def route_token(token, target_frequency, target_amplitude):
    """
    Simulates routing the token through a field layer.
    """
    token.set_field_state(target_frequency, target_amplitude)
    return token.describe()

def adjust_fluorescence(token, add_tag=None, clear=False):
    """
    Adds or clears fluorescence tags from a token.
    """
    if clear:
        token.clear_fluorescence()
    elif add_tag:
        token.add_fluorescence(add_tag)
    return token.describe()

def shift_token_q_state(token, new_q_state):
    """
    Change the Q-layer state of a token (-1, 0, +1)
    """
    token.shift_q_state(new_q_state)
    return token.describe()

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
