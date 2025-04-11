import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import json

def load_token_vectors(path="token_influence_vectors.npy"):
    return np.load(path)

def load_token_log(path="../memory/token_trail_log.json"):
    with open(path, "r") as f:
        return json.load(f)

def visualize_token_map(token_vectors, token_log):
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(token_vectors)

    plt.figure(figsize=(10, 8))
    plt.scatter(reduced[:, 0], reduced[:, 1], c="gray", alpha=0.4, label="All Tokens")

    # Highlight tokens from the log
    for entry in token_log:
        idx = entry["input_index"]
        x, y = reduced[idx]
        plt.scatter(x, y, c="red")
        plt.text(x + 0.01, y + 0.01, f"{idx}", fontsize=8, color="red")

    plt.title("Token Trail Map")
    plt.xlabel("PCA-1")
    plt.ylabel("PCA-2")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("token_map.png")
    print("Token map saved to token_map.png")

def main():
    token_vectors = load_token_vectors()
    token_log = load_token_log()
    visualize_token_map(token_vectors, token_log)

if __name__ == "__main__":
    main()
