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

## Token Meaning Mapper

Filename: token_meaning_mapper.py
Location: /opt/ai-core/tools
Created: 2025-04-12 12:47:45 UTC

Description:
The Token Meaning Mapper tool visualizes the directional relationship between input and output tokens from training pairs. Each pair is treated as a "thought movement" from one token to another, capturing the difference vector and reducing it using PCA for visualization.

Input:
../tokenizer/full_color_tokens.csv: The color-token vectors.

../training/training_pairs.py: A list of manually defined training token index pairs.

Output:
A 2D PCA projection of token meaning transitions saved as token_meaning_map.png.

Usage:

cd /opt/ai-core/tools
python3 token_meaning_mapper.py

Visualization Notes:
Each dot represents the direction from a source token to its paired target token.

Example:

Red 40 → 60

Blue 10 → 25

Green 20 → 35

Orange 15 → 30

Purple 50 → 70

The arrows or directions help indicate how tokens semantically transition during model training.

---------------------------------------------------------------------------------------------------------

## generate_training_set_from_tokens.py

- Converts structured color token data from `tokenizer/full_color_tokens.csv`
- Extracts RGB values and builds token pairs
- Default: pulls 10 samples per run
- Output: `training/training_set.csv` (overwrites each time)

--------------------------------------------------------------------------------


---

### 📁 `tools/README.md`

```markdown
## Tool: merge_trait_memory_formats.py

**Purpose:** Upgrades legacy trait logs to dual-format compatibility.

### Function:
- Loads legacy list-format trait memory
- Wraps it into a dict format with:
  - `linked_phases`
  - `trait_evolution`
  - `history` (original array preserved)

### Output:
- Replaces `memory/trait_memory_log.json` with upgraded format
- Backs up original to `memory/trait_memory_log_backup.json`

### Notes:
- Ensures compatibility for both list-style and structured memory tools
- Should only be run once (or if format reset is required)

________________________________________________________________________________

Add: generate_training_set_from_tokens_fixed.py, describe conversion purpose.

## Tools Added in Phase 35.2

### `generate_training_set_from_tokens_fixed.py`
- Converts `full_color_tokens.csv` into a fully structured `training_set.csv`.
- Filters malformed rows and extracts `input_token`, `target_token`, `label`, and `weight`.
- Output: `training/training_set.csv`

### `batch_token_trainer_fixed.py`
- Processes token batches in 10-token groups.
- Runs 10 epochs per batch.
- Logs output to `training/training_output_log.json`.
- Includes debug output, reflection pauses, and loss tracking.
""",