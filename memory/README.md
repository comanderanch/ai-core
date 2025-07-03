# memory
Description for the memory directory.

# Memory

This is the long-term and short-term memory layer of the AI system.

## Purpose
- Store facts, events, and learned experiences over time.
- Act as the internal knowledge base accessed during reasoning.
- Track past inputs, context history, and evolving concepts.

## Structure (Planned)
- `static/` – BIOS-like foundational data (hardcoded truths).
- `dynamic/` – Runtime-learned data and evolving structures.
- `nodes/` – Organized memory chunks (node-based architecture).
- `index.json` – Lookup and metadata about memory structure.

## Features
- Each memory node can reference others (graph-style).
- Supports tagging with frequency, importance, or recency.
- Allows pruning, merging, or rewriting during training cycles.

## Notes
Memory is a core component for contextual continuity.  
It may interface directly with `ai-engine` for thought recall and learning.

# Memory System

This directory stores token activity logs for the AI-Core minimal LLM.

## Files

- `token_trail_log.json`  
  Contains timestamped logs of token activity including input index, output vector summary (mean, max, min), and contextual metadata.

## Phase Reference
- Introduced in Phase 5.7: Token Trail Mapping and Memory Simulation.
- Used during inference to track LLM behavior and token flow.

_____________________________________________________________

- `train_model_from_csv.py` – Loads CSV data and simulates minimal token-based learning with label association output.

_____________________________________________________________

### label_trait_loader.py

- Loads label ➜ trait mappings from `label_trait_map.json`.
- Maps each label to a reflex trigger and memory bias score.
- Used to inform learning traits in Phase 33 association processing.

✅ Status: Complete (Phase 33.2)

_______________________________________________________________

### memory_bias_injector.py

- Records and stores trait-related memory bias changes based on labeled training associations.
- Outputs to `memory_bias_log.json` with label and bias value.
- Used in runtime to inform AI reflex leanings and reinforcement tendencies.

✅ Status: Complete (Phase 33.3.3)

___________________________________________________________________

### Memory Outputs (Generated)

- `label_trait_map.json` – Defines label ➜ trait ➜ bias associations.
- `memory_bias_log.json` – Records injected bias per label.

____________________________________________________________________

New files:

label_trait_loader.py — Loads label-to-trait mappings from JSON.

label_trait_map.json — Contains label ➝ trait ➝ reflex ➝ memory bias mapping table.

memory_bias_injector.py — Injects memory bias values associated with labeled tokens.

memory_bias_log.json — Records all memory bias injections chronologically.

reflex_response_log.json — Stores all reflex responses triggered from label mapping during inference.

reflex_weight_adjustments.json — Reflects calculated strength of reflex triggers from log frequency.

_____________________________________________________________________________

### Reflex Weight & Reinforcement Logs

- `reflex_response_log.json` — Raw log of reflex responses triggered.
- `reflex_influence_summary.json` — Reflex frequency aggregation.
- `reflex_weight_log.json` — Reflex weights used in influence calculations.
- `reflex_reinforcement_log.json` — Record of reinforcement adjustments to reflex weights.

____________________________________________________________________________

- `reflex_response_score.json` — Stores the final score reflecting reflex alignment strength.

____________________________________________________________________________

- `reflex_adaptation_log.json` — Stores trend outcomes from adaptation analysis. Indicates whether reflexes are strengthening, weakening, or stabilizing.

___________________________________________________________________________

- `reflex_drift_log.json` — Logs any detected drift between bias and weight for reflex actions.

_____________________________________________________________________________

- `reflex_stability_log.json` — Logs per-reflex stability scoring derived from bias/weight evaluations.

_____________________________________________________________________________

- `reflex_drift_log.json` — Records calculated drift values between expected (bias) and observed (weight) reflex responses. Includes timestamps, labels, and deviation magnitude.

_____________________________________________________________________________

- `reflex_drift_log.json` — Logs drift values (bias vs weight) over time.
- `reflex_correction_log.json` — Logs corrective adjustments to reflex weights after drift detection.

______________________________________________________________________________

### reflex_weight_sync_log.json

Stores timestamped snapshots of all reflex weights. This serves as a historical ledger for weight evolution over time and supports trend monitoring or rollbacks.

_____________________________________________________________________________

### reflex_convergence_log.json
Stores the convergence trend of each reflex based on historical weight snapshots. Includes timestamp, weight variability, and stability trend.

________________________________________________________________________________

- `reflex_drift_log.json`: Logs calculated drift between a reflex's expected bias and current weight.
- `reflex_correction_log.json`: Stores adjustments made to reflex weights to reduce drift.
- `reflex_weight_sync.json`: Snapshot of the most recent synchronized reflex weights.
- `reflex_convergence_log.json`: Tracks how reflex weights stabilize over time.

_________________________________________________________________________________


---

### 📁 `memory/README.md`

```markdown
## trait_memory_log.json

**Purpose**:  
Tracks finalized combinations of label, reflex, and trait for long-term memory mapping.

**Structure**:
- `timestamp`: When the memory was reinforced.
- `trait_id`: Unique identifier composed of label, reflex, and trait.
- `label`: The input token's meaning.
- `reflex`: The triggered response.
- `trait`: The associated behavior pattern.
- `bias`: Final learned bias.
- `weight`: Final stabilized reflex weight.

**Sample Entry**:
```json
{
    "timestamp": "2025-07-03T18:57:33.374931",
    "trait_id": "Growth:explore_mode:curiosity_trigger",
    "label": "Growth",
    "reflex": "explore_mode",
    "trait": "curiosity_trigger",
    "bias": 0.9,
    "weight": 0.9
}

_____________________________________________________________________

### trait_relationship_map.json

A dictionary mapping each trait to:
- All labels that use it
- All reflexes linked with it

Example:
```json
{
  "curiosity_trigger": {
    "labels": ["Growth"],
    "reflexes": ["explore_mode"]
  }
}

________________________________________________________________________

