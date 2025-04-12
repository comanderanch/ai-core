import os
import numpy as np
import csv
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import importlib.util

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

def load_training_pairs(path="../training/training_pairs.py"):
    spec = importlib.util.spec_from_file_location("training_pairs_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.training_pairs

def map_token_meanings(tokens, pairs):
    output_vectors = []
    labels = []
    for i, j in pairs:
        labels.append(f"{i}->{j}")
        diff = tokens[j] - tokens[i]
        output_vectors.append(diff)
    return np.array(output_vectors), labels

def visualize_meaning_map(vectors, labels, output_path="token_meaning_map.png"):
    pca = PCA(n_components=2)
    projected = pca.fit_transform(vectors)

    plt.figure(figsize=(10, 8))
    for i, label in enumerate(labels):
        x, y = projected[i]
        plt.plot(x, y, 'o')
        plt.text(x, y, label, fontsize=7, alpha=0.7)

    plt.title("Token Meaning Mapper (Token Influence Direction)")
    plt.xlabel("PCA Dimension 1")
    plt.ylabel("PCA Dimension 2")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"✅ Meaning map saved to {output_path}")

def main():
    tokens = load_tokens()
    pairs = load_training_pairs()
    vectors, labels = map_token_meanings(tokens, pairs)
    visualize_meaning_map(vectors, labels)

if __name__ == "__main__":
    main()
