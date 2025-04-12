import numpy as np
import matplotlib.pyplot as plt
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import csv

def load_token_log(path="../memory/token_trail_log.json"):
    with open(path, "r") as f:
        return json.load(f)

def load_tokens(csv_path="../tokenizer/full_color_tokens.csv"):
    tokens = []
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            hue_bin, r_bin, g_bin, b_bin, frequency = row[:5]
            token_vec = [int(b) for b in hue_bin + r_bin + g_bin + b_bin]
            token_vec.append(float(frequency))
            tokens.append(token_vec)
    return np.array(tokens)

def visualize_token_paths(token_log, tokens):
    indices = [entry["input_index"] for entry in token_log]
    unique_indices = sorted(set(indices))

    if len(unique_indices) < 2:
        print("❌ Not enough unique tokens in log to visualize a path (need at least 2).")
        return

    token_vectors = tokens[unique_indices]
    pca = PCA(n_components=2)
    projected = pca.fit_transform(token_vectors)

    plt.figure(figsize=(10, 8))
    for i, idx in enumerate(unique_indices):
        x, y = projected[i]
        plt.plot(x, y, 'o', label=f"Token {idx}", alpha=0.7)
        plt.text(x, y, str(idx), fontsize=8, alpha=0.6)

    plt.title("Token Path Tracker (Token Activity Over Time)")
    plt.xlabel("PCA Dimension 1")
    plt.ylabel("PCA Dimension 2")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("token_path.png")
    print("✅ Token path visualization saved to token_path.png")

# ENTRYPOINT
if __name__ == "__main__":
    token_log = load_token_log()
    tokens = load_tokens()
    visualize_token_paths(token_log, tokens)
