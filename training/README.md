# Training Module – AI-Core

This folder contains manual training pair definitions used to test the minimal LLM with custom color tokens.

### Files:
- `training_pairs.py` – A list of manually defined (input index, target index) training pairs. These map tokens from `full_color_tokens.csv` to simulate early-stage language patterns.

### Purpose:
To validate that token inputs from the custom CSV can flow through the minimal model, and that predictable outputs are produced from structured input pairs.

This is the first step toward full-scale LLM training using color-based token systems.
---------------------------------------------------------------------------------------------------------------------------

Add: generate_training_set_from_tokens_fixed.py and the 2000-token training loop logic with controlled batching and phase output.

sorry i mised some steps full reports will be provided as files grow .added tools with greate abilitys that basicaly speak for there selfs entering dual cognition and security layer logic  color spectrum now incresed from full spectrum of 6+setilion to double with sum of 13+ sextilion dual layer with 
converted values and raw token states

## Training Phase 35.2 – Dual Cognition Prep

- Introduced `training_set.csv` containing 5.3M token pairs generated from `full_color_tokens.csv`.
- Ran the first 2000-token batch with 10-token segments over 10 epochs each.
- Log output stored in `training_output_log.json`, capturing per-phase loss convergence and stability.
- Training script: `tools/batch_token_trainer_fixed.py` (handles incremental batch logic, logs, and pause intervals).
""",

----------------------------------------------------------------------------------------------------