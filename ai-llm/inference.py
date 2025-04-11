import sys
import numpy as np
import os
from minimal_llm import MinimalLLM, load_tokens
from training.training_pairs import training_pairs
from sklearn.metrics.pairwise import cosine_similarity
from memory.token_trail import log_token_activity

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 inference.py <token_index>")
        return

    index = int(sys.argv[1])

    # Load tokens with influence vectors
    tokens = load_tokens("../tokenizer/full_color_tokens.csv", "token_influence_vectors.npy")
    model = MinimalLLM(input_size=tokens.shape[1], hidden_size=8, output_size=tokens.shape[1])

    # Load trained weights
    data = np.load("model_weights.npz")
    model.W1 = data["W1"]
    model.b1 = data["b1"]
    model.W2 = data["W2"]
    model.b2 = data["b2"]
    print("Model loaded from saved weights.")

    test_input = tokens[index].reshape(1, -1)
    prediction = model.forward(test_input)
    print("Model prediction:", prediction)

    log_token_activity(index, prediction)

    # Compare to the target token
    target_idx = next((t[1] for t in training_pairs if t[0] == index), None)
    if target_idx is not None:
        target_vector = tokens[target_idx].reshape(1, -1)
        score = cosine_similarity(prediction, target_vector)[0][0]
        print(f"Cosine Similarity to target token: {score:.4f}")

    else:
        print("No matching target found in training_pairs.")

    # Automatically regenerate token map
    os.system("python3 token_map.py")

if __name__ == "__main__":
    main()
