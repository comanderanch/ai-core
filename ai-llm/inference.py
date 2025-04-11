import numpy as np
from minimal_llm import MinimalLLM, load_model, load_tokens
from training.training_pairs import training_pairs

# Load token data
tokens = load_tokens("../tokenizer/full_color_tokens.csv")

# Initialize and load trained model
model = MinimalLLM(input_size=tokens[0].shape[0], hidden_size=8, output_size=tokens[0].shape[0])
load_model(model)
print("Model loaded from saved weights.")

# Pick a token to test (unseen or known)
test_index = training_pairs[0][0]  # Replace with any index you want to test
test_input = tokens[test_index].reshape(1, -1)

# Get model output
prediction = model.forward(test_input)
print("Model prediction:", prediction)
