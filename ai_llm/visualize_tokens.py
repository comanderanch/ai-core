import numpy as np
import matplotlib.pyplot as plt
from minimal_llm import load_tokens

# Load token vectors (with frequency included)
tokens = load_tokens("../tokenizer/full_color_tokens.csv")

# Reduce dimensionality with PCA
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
token_2d = pca.fit_transform(tokens)

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(token_2d[:, 0], token_2d[:, 1], s=10, alpha=0.7, c='skyblue', edgecolors='k')
plt.title("Token Space Projection (PCA - 2D)")
plt.xlabel("Component 1")
plt.ylabel("Component 2")
plt.grid(True)
plt.tight_layout()
plt.savefig("token_projection.png")
print("Token visualization saved to token_projection.png")
