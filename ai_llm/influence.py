import numpy as np
from sklearn.neighbors import NearestNeighbors
from minimal_llm import load_tokens

def compute_token_influences(csv_path, k=5):
    tokens = load_tokens(csv_path)

    nbrs = NearestNeighbors(n_neighbors=k+1, algorithm='auto').fit(tokens)
    distances, indices = nbrs.kneighbors(tokens)

    influences = []

    for i in range(len(tokens)):
        neighbor_ids = indices[i][1:]  # exclude self
        neighbor_vectors = tokens[neighbor_ids]
        influence_vector = np.mean(neighbor_vectors, axis=0)
        influences.append(influence_vector)

    return np.array(influences)

if __name__ == "__main__":
    tiv = compute_token_influences("../tokenizer/full_color_tokens.csv")
    np.save("token_influence_vectors.npy", tiv)
    print("Token influence vectors saved to token_influence_vectors.npy")
