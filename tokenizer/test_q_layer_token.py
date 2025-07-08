# test_q_layer_token.py

from q_layer_token import QLayerToken

# Create a token with base red color
token = QLayerToken(base_color=(255, 0, 0))

# Set field state
token.set_field_state(frequency=13.5, amplitude=0.72)

# Add fluorescence
token.add_fluorescence("logic")
token.add_fluorescence("memory")

# Shift Q-state to +1 (conscious)
token.shift_q_state(+1)

# Print token description
print("Token Description:")
print(token.describe())
