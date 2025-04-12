import numpy as np
from sklearn.metrics.pairwise import cosine_distances
import matplotlib.pyplot as plt

def load_tokens(path):
    tokens = []
    with open(path, 'r') as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split(',')
            # hue_bin, r_bin, g_bin, b_bin, frequency
            hue = [int(b) for b in parts[0]]
            r = [int(b) for b in parts[1]]
            g = [int(b) for b in parts[2]]
            b = [int(b) for b in parts[3]]
            freq = [float(parts[4])]
            token = hue + r + g + b + freq
            tokens.append(token)
    return np.array(tokens)

def detect_anomalies(tokens, threshold=2.0):
    distances = cosine_distances(tokens)
    mean_distances = np.mean(distances, axis=1)
    z_scores = (mean_distances - np.mean(mean_distances)) / np.std(mean_distances)
    anomaly_indices = np.where(np.abs(z_scores) > threshold)[0]
    return anomaly_indices, z_scores

def main():
    token_file = "../tokenizer/full_color_tokens.csv"
    tokens = load_tokens(token_file)
    anomalies, z_scores = detect_anomalies(tokens)

    print(f"Detected {len(anomalies)} anomalous tokens:")
    for idx in anomalies:
        print(f"Token {idx} → z-score = {z_scores[idx]:.2f}")

    # Optional: Plot Z-scores
    plt.figure(figsize=(12, 4))
    plt.plot(z_scores, label="Z-score")
    plt.axhline(y=2.0, color='r', linestyle='--', label="Threshold")
    plt.axhline(y=-2.0, color='r', linestyle='--')
    plt.title("Token Anomaly Z-Scores")
    plt.xlabel("Token Index")
    plt.ylabel("Z-Score")
    plt.legend()
    plt.tight_layout()
    plt.savefig("token_anomalies.png")
    print("Saved plot to token_anomalies.png")

if __name__ == "__main__":
    main()
