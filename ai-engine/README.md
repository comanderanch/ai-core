# ai-engine
Description for the ai-engine directory.

# AI Engine

This is the core logic layer of the AI system.  
It handles the thinking, decision-making, and state transitions.

## Purpose
The AI Engine is responsible for:

- Interpreting tokenized input (color-based or traditional)
- Generating output decisions or actions
- Interfacing with memory nodes and feedback loops
- Switching between processing modes or internal "states"

## Components (Planned)
- `core.cpp` / `core.py` – Main processing loop
- `state_manager.*` – Controls attention, context, and AI modes
- `evolution.*` – Handles self-evolving routines and refinements
- `hooks/` – Optional logic injections or runtime modifiers

## Notes
This layer stays mostly "logic-pure" — no UI, no storage, just pure reasoning.  
Everything else (memory, tokenizer, configs) feeds into this.

_____________________________________________________________________

---

## 🧠 Journal Update – Phase 33 Summary

**Checkpoint:** Reflex Conditioning + Bias Injection  
**Status:** ✅ Complete  

- Label ➝ Trait ➝ Reflex mapping system added.
- Structured training now uses `training_set.csv`.
- Reflex triggers are logged and analyzed for weight adjustments.
- Memory bias logic supports dynamic reflex reinforcement.

All modules updated, logged, and version-controlled.

________________________________________________________________________

### Phase 33.7 – Reflex Drift Handler

- Implemented `reflex_drift_handler.py` to calculate and log drift between bias and reflex response.
- Output stored in `memory/reflex_drift_log.json`.
- This module enables tracking of long-term behavioral accuracy and adaptation need.

________________________________________________________________________

All Phases up are confirmed in scripts README.md

### Completed: Phase 35.0 – Training Bootstrap

Status: ✅ Verified
Next: Phase 35.1 – Controlled Training Execution

✅ Log verified.

Final confirmation:

"training_status": "data_loaded" → ✔

"sample_count": 3 → ✔

"errors": [] → ✔

"start_time" still null → ✔ (expected since no training yet)

"output_summary" placeholder → ✔

This confirms that Phase 35.0 bootstrap completed successfully, with no faults or partial states.

You may now proceed to next step in Phase 35.--.

---------------------------------------------------------
### Phase 35.1 – Controlled Training Execution

- Model: MinimalLLM
- Input: 3 token pairs (CSV)
- Epochs: 10
- Loss dropped from 6.41 → 0.0064
- Status: ✅ Completed and logged

---------------------------------------------------------

### Training Dataset Management

- Original token training set (3 samples) has been archived as: `training/training_set_original.csv`
- Token generator script added: `tools/generate_training_set_from_tokens.py`
  - Pulls 10-token batches from `tokenizer/full_color_tokens.csv`
  - Converts raw color rows into `input_token`, `target_token`, `label`, and `weight`
- Current training set is auto-regenerated for each training run

-----------------------------------------------------------------

### Phase 35.2 – Batch Training Execution

- Appended the training script to support sequential token batch loading.
- Added structured phase logging to `training_output_log.json`.
- Training is now tracked per phase, with loss history recorded for each.
- Verified training success using new `training_set.csv` with 9 color token entries.
- Final loss: `0.0508` over 10 epochs.

🕒 Completed: 2025-07-07

--------------------------------------------------------------

