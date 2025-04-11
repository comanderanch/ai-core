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

# Load target token for comparison (same as training target)
from training.training_pairs import training_pairs
target_index = [pair[1] for pair in training_pairs if pair[0] == test_index]

if target_index:
    target_vector = tokens[target_index[0]].reshape(1, -1)
    from minimal_llm import cosine_similarity
    score = cosine_similarity(prediction, target_vector)
    print(f"Cosine Similarity to target token: {score:.4f}")
else:
    print("No associated target found for this token.")
