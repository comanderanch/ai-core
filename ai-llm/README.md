Minimal LLM- AI-Core
This module is a NumPy-based minimal LLM used to test integration of custom binary tokens.

Files:
minimal_llm.py - Loads tokens from CSV and runs a forward pass through a simple feedforward network.

../tokenizer/full_color_tokens.csv - Custom token set generated from hue, RGB, and frequency values.

How to Run:

python3 minimal_llm.py

Output:
Prints the token input vector

Prints the model output vector

This confirms the connection between the color-token CSV and the model input.

- Calculates loss using mean squared error for each training pair

- Implements train_step with gradient descent to adjust model weights per input/output pair

- Supports multiple epochs of training using custom token input pairs
