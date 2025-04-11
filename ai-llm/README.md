Minimal LLM- AI-Core
This module is a NumPy-based minimal LLM used to test integration of custom binary tokens.

Files:
minimal_llm.py - Loads tokens from CSV and runs a forward pass through a simple feedforward network.

../tokenizer/full_color_tokens.csv - Custom token set generated from hue, RGB, and frequency values.

How to Run:

python3 minimal_llm.py

Output:
Prints the token input vector

Prints the model output vector

This confirms the connection between the color-token CSV and the model input.

- Calculates loss using mean squared error for each training pair

- Implements train_step with gradient descent to adjust model weights per input/output pair

- Supports multiple epochs of training using custom token input pairs

- Model state can be saved and reloaded using `save_model()` and `load_model()`

- Reloaded models can make predictions without retraining


## Inference

- `inference.py` loads the trained model and runs predictions on token input.
- Uses saved weights from `model_weights.npz`.
- Demonstrates how the LLM can operate independently from training.

- Supports command-line token index selection:
  `python3 inference.py <index>`

## Evaluation

- `evaluate.py` runs the model against all known training pairs.
- Outputs individual loss and average loss across the dataset.
- Useful for verifying model retention and performance after training.

- Calculates cosine similarity between model output and associated target token.
- Allows quantitative evaluation of learned associations.

## Token Enrichment

- Token vectors now include a normalized frequency component (41D total).
- Frequency serves as an added context dimension, improving semantic similarity.
- Cosine similarity increased after retraining, verifying deeper pattern alignment.

## Token Space Visualization

- Tokens were projected to 2D space using PCA for inspection.
- The result shows diagonal variance, distributed clusters, and strong spacing.
- Confirms token structure integrity across RGB, Hue, and Frequency dimensions.
- Visualization saved as: `token_projection.png`

## Token Influence Vectors (TIV)

- Introduced Phase 5.4: Each token now includes influence from its 5 nearest neighbors.
- This expands tokens from 41D → 82D, combining identity and local context.
- Result: smoother learning curves and enhanced memory potential.
- Influence vectors saved as: `token_influence_vectors.npy`

## Visualization

- PCA projection of all tokens confirms structured distribution.
- Chart: `token_projection.png`

## Phase 5.5 — Influence-Aware Inference & Similarity Scoring

- Inference updated to include Token Influence Vectors (TIV) in model input.
- Cosine similarity is now calculated between prediction and expected target token.
- Allows evaluation of semantic accuracy in high-dimensional token space.
- Example result:


- Script: `inference.py`
- Influence vectors: `token_influence_vectors.npy`
