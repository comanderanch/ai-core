# tools
Description for the tools directory.

# Tools

This directory contains utilities that support development, debugging, and performance tuning.

## Purpose
- Provide standalone helper scripts for inspecting, testing, or modifying AI subsystems.
- Accelerate development with reusable functions and diagnostic tools.
- Isolate non-core logic that doesn’t belong in the main engine.

## Contents (Examples)
- `inspector.py` – View token streams, memory traces, or reasoning chains.
- `profiler.py` – Benchmark timing and CPU/memory usage per module.
- `patcher.py` – Inject or modify parts of the engine during live sessions.
- `validator.py` – Check token integrity, config sanity, and memory references.

## Notes
These tools are optional but highly recommended for serious development and debugging.  
They are isolated to avoid interfering with core engine logic and allow safe experimentation.

### Token Cluster Detector

**File:** `token_cluster_detector.py`  
**Purpose:** Analyzes cosine similarity between color tokens to identify natural clusters.  
**Output:** `token_clusters.png` — A visual map showing cluster formations and alignment paths between tokens.  
**Notes:** Used for identifying emergent token relationships and validating anchor influence on spatial structure.

# Token Anomaly Detector

This tool scans the full set of token vectors and detects anomalies based on z-score analysis. Tokens with significantly higher or lower average activation values are flagged for review.

## How It Works

- Loads all token vectors from `../tokenizer/full_color_tokens.csv`.
- Computes the average (mean) value for each token vector.
- Calculates z-scores across all means.
- Flags any token whose z-score is > 2 or < -2 as an anomaly.
- Visualizes the full distribution and highlights anomaly zones.

## Output

- **Console**: List of anomalous token indices and their z-scores.
- **Image**: `token_anomalies.png` is generated and saved in the same folder.

## Usage

From inside the `/tools` directory:

```bash
python3 token_anomaly_detector.py

Tool: Token Path Tracker (token_path_tracker.py)
This tool visualizes the trail of token predictions over time using PCA for dimensionality reduction.
Each token logged through inference.py is mapped and labeled on a 2D coordinate plane.
It helps identify behavioral shifts, token prediction consistency, and memory pathing.

Output: token_path.png
Example visualization:

Token 20 appears in green at (0.0, 1.25)

Token 15 in orange near top-left at (0.6, 0.50)

Another Token 20 in blue around bottom-left at (-0.6, -0.50)

