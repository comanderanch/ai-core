# scripts
Description for the scripts directory.

# Scripts

This directory contains all helper scripts used to run, test, train, or maintain the AI system.

## Purpose
- Automate repetitive tasks like bootstrapping, testing, or memory cleanup.
- Serve as a glue layer between components (engine, tokenizer, memory).
- Support development, deployment, and debugging workflows.

## Typical Scripts (Planned)
- `train.sh` – Runs a full training cycle.
- `start.sh` – Boots up the AI system in the desired state.
- `reset.sh` – Clears dynamic memory or session logs.
- `debug.py` – Tools for inspecting state and internal variables.
- `upgrade.py` – Handles evolutionary jumps or patch routines.

## Notes
Scripts should be modular and well-commented.  
Avoid hardcoding paths; use relative paths and environment configs where possible.

Scripts should be executable (`chmod +x`) and tested in isolation before inclusion in the main workflow.

# AI-Core Scripts

This directory contains the scripts for the **AI-Core** project. These scripts implement the various stages of the AI system, including decision-making, behavior triggering, and autonomous reflexes.

## Scripts Overview

1. **`decision_chain_manager.py`**:
   - Handles the logic for processing token events and triggering actions based on token activity.

2. **`behavior_trigger_system.py`**:
   - Triggers actions based on the decisions made in the decision chain and updates the system's memory.

3. **`autonomous_reflex_behavior.py`**:
   - Implements reflexive behavior based on token events and updates the internal state based on patterns of token activity.

## Setup

Ensure that the necessary dependencies are installed by running:
```bash
pip3 install -r requirements.txt


Running the Scripts
You can run each script individually:


python3 decision_chain_manager.py
python3 behavior_trigger_system.py
python3 autonomous_reflex_behavior.py


Future Work
Enhancing the reflexive behavior system

Integrating the system with additional components of the AI framework


## token_reflex_loop.py

**Purpose:**  
Scans token trail data and identifies reflex loops — repeated appearances of the same token across trail passes. This allows the system to detect potential reinforcing nodes, recursive memory references, or structural loops in token behavior.

**Functionality:**
- Analyzes existing token trail data for reoccurrences.
- Tallies how many times each token appears in a looped sequence.
- Outputs a structured JSON array showing each reflexive token and its count.

**Example Output:**
```json
[
    { "token": 10, "count": 2 },
    { "token": 15, "count": 2 },
    { "token": 20, "count": 2 }
]

json saved in memory ~/ai-core/memory/reflex_tokens_log.json

## cognitive_reflex_engine.py

**Purpose:**  
Serves as the central integration engine for Phase 7. It consumes token reflex data and triggers behavior and decision modules based on high-frequency reflexive tokens.

**Functionality:**
- Loads `reflex_tokens_log.json` and `token_trail_log.json`
- Identifies tokens with reflex counts above threshold
- Triggers mapped behavior routines (e.g., memory updates, logic actions)
- Builds decision chains via the decision manager for reflex tokens

**Trigger Conditions:**
- Tokens like `20` trigger "Action A"
- Tokens like `40` (when mapped) trigger "Action B"
- Unmapped tokens are ignored gracefully

**Modules Called:**
- `behavior_trigger_system.trigger_from_tokens()`
- `decision_chain_manager.construct_from_reflex()`

**Run Command:**
```bash
python3 scripts/cognitive_reflex_engine.py


## Reflex Feedback Logging (Phase 7.1)

**Overview:**  
The behavior system now logs every triggered reflex action into `reflex_feedback_log.json`.  
This marks the first instance of **cognitive memory recording**, allowing the AI to retain awareness of its decisions over time.

**Log File:**  
`memory/reflex_feedback_log.json`

**Log Structure:**
```json
[
    {
        "action": "Trigger Action A",
        "timestamp": "2025-04-15T02:52:26.945349Z"
    }
]
