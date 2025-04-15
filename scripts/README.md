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