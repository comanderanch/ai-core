import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_token_log(path="token_trail_log.json"):
    if not os.path.exists(path):
        print(f"Log file not found: {path}")
        return []
    with open(path, "r") as f:
        return json.load(f)

def extract_output_vectors(log_data):
    return np.array([entry["output_summary"]["mean"] for entry in log_data])

def generate_heatmap(values, save_path="token_heatmap.png"):
    sns.set()
    plt.figure(figsize=(12, 1.5))
    sns.heatmap([values], cmap="viridis", cbar=True, xticklabels=False, yticklabels=False)
    plt.title("Token Activity Frequency Heatmap")
    plt.savefig(save_path)
    print(f"Heatmap saved to {save_path}")

def main():
    log_data = load_token_log("token_trail_log.json")
    if not log_data:
        return

    output_means = extract_output_vectors(log_data)
    generate_heatmap(output_means)

if __name__ == "__main__":
    main()
