import numpy as np
import csv
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def load_tokens(csv_path):
    tokens = []
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            hue_bin = row[0]
            r_bin = row[1]
            g_bin = row[2]
            b_bin = row[3]
            token = [int(b) for b in hue_bin + r_bin + g_bin + b_bin]
            frequency = float(row[4])
            token.append(frequency)
            tokens.append(token)
    return np.array(tokens)

def main():
    tokens = load_tokens("../tokenizer/full_color_tokens.csv")

    # Reduce dimensionality for clustering
    pca = PCA(n_components=10)
    reduced_tokens = pca.fit_transform(tokens)

    # Run fast KMeans clustering
    kmeans = KMeans(n_clusters=10, random_state=42, n_init='auto')
    labels = kmeans.fit_predict(reduced_tokens)

    # Visualize with PCA projection to 2D
    proj = PCA(n_components=2).fit_transform(tokens)

    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(proj[:, 0], proj[:, 1], c=labels, cmap="tab10", s=10)
    plt.title("Token Cluster Visualization")
    plt.colorbar(scatter)
    plt.tight_layout()
    plt.savefig("token_clusters.png")
    print("Token clusters saved to token_clusters.png")

if __name__ == "__main__":
    main()
