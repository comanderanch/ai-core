import numpy as np
import csv
from sklearn.metrics.pairwise import cosine_similarity

# Load tokens from CSV (skip header)
def load_tokens(csv_path):
    tokens = []
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            hue_bin, r_bin, g_bin, b_bin, *_ = row
            token_vec = [int(b) for b in hue_bin + r_bin + g_bin + b_bin]
            tokens.append(token_vec)
    return np.array(tokens)

# Compute cosine similarity and extract top-N anchors
def compute_anchors(tokens, top_n=5):
    similarity = cosine_similarity(tokens)
    anchors = []

    for i in range(len(tokens)):
        # Get top N (excluding self)
        sims = similarity[i]
        top_indices = np.argsort(sims)[::-1][1:top_n+1]
        anchors.append(top_indices.tolist())

    return np.array(anchors)

# Save anchors as .npy for easy loading
def save_anchors(anchor_matrix, path="token_anchors.npy"):
    np.save(path, anchor_matrix)
    print(f"Anchors saved to {path}")

if __name__ == "__main__":
    tokens = load_tokens("full_color_tokens.csv")
    anchors = compute_anchors(tokens, top_n=5)
    save_anchors(anchors)
