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

## Phase 5.6: Token Anchor Reinforcement Training

In this phase, the LLM was trained using **anchored context influence** from token space.

### Key Additions:
- Introduced `token_anchors.npy`: a file mapping each token to its N nearest semantic neighbors.
- Modified `minimal_llm.py` to blend token input with its anchor average.
- Training now incorporates **anchor-based contextual smoothing**.

### Observations:
- Training loss consistently decreased.
- Cosine similarity score for test token increased from `0.0124` → `0.0442`
- This confirms **vector awareness** and **multi-token influence dynamics**.

> The model is showing signs of **relational generalization**, even at minimal scale.

- Added anchor-based reinforcement to training (Phase 5.6)
- Integrated token trail logging (Phase 5.7)

Phase 5.7 — Token Trail Mapping
Objective:
Track how token outputs evolve during training and inference, and generate visual maps of token activation and prediction paths.

Key Features Added:

token_trail.py in /memory:

Logs token activity (timestamp, input index, summary stats like mean/max/min).

Writes to token_trail_log.json.

inference.py (Enhanced):

Calculates cosine similarity between predicted and target token.

Calls the logger on each run.

Auto-generates an updated token map using token_map.py.

token_map.py in ai-llm:

Visualizes the latest log of token activity.

Saves a PNG token_map.png to reflect prediction traces.

Run Example:

``` python3 inference.py 10 ```

Outputs:

Cosine similarity score

JSON log entry (memory/token_trail_log.json)

Regenerated token_map.png
