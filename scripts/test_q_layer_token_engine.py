# test_q_layer_token_engine.py

from q_layer_token import (
    generate_q_token,
    route_token,
    adjust_fluorescence,
    shift_token_q_state
)

# Step 1: Create a token
token = generate_q_token(base_color=(128, 0, 255), tag_list=["init"], mode="propagate")
print("\n[Step 1] Generated Token:")
print(token.describe())

# Step 2: Adjust fluorescence
desc_fluor = adjust_fluorescence(token, add_tag="logic")
print("\n[Step 2] Added 'logic' Fluorescence:")
print(desc_fluor)

# Step 3: Shift Q-state to +1 (conscious)
desc_q = shift_token_q_state(token, +1)
print("\n[Step 3] Shifted Q-State to +1:")
print(desc_q)

# Step 4: Route with frequency and amplitude
desc_routed = route_token(token, target_frequency=22.4, target_amplitude=0.94)
print("\n[Step 4] Routed Token with EM Field:")
print(desc_routed)
