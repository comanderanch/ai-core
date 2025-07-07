import numpy as np
from minimal_llm import MinimalLLM, load_model, load_tokens, mean_squared_error
from training.training_pairs import training_pairs

# Load model and tokens
tokens = load_tokens("../tokenizer/full_color_tokens.csv")
model = MinimalLLM(input_size=tokens[0].shape[0], hidden_size=8, output_size=tokens[0].shape[0])
load_model(model)
print("Model loaded.")

# Evaluate on all training pairs
total_loss = 0
for i, (input_idx, target_idx) in enumerate(training_pairs):
    input_sample = tokens[input_idx].reshape(1, -1)
    target_sample = tokens[target_idx].reshape(1, -1)

    output = model.forward(input_sample)
    loss = mean_squared_error(output, target_sample)
    total_loss += loss
    print(f"Pair {i+1}: Loss = {loss:.6f}")

# Average loss
avg_loss = total_loss / len(training_pairs)
print(f"\nAverage Loss: {avg_loss:.6f}")
