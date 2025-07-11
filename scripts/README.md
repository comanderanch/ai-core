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

## Phase 7.3 — Weighted Reflex Cognition

**Overview:**  
The AI now evaluates its own behavior patterns and makes decisions based on past frequency of actions.  
This introduces **reflex bias** — a primitive form of reinforcement learning based on logical memory, not prediction.

**What It Does:**
- Loads behavior summary from `memory/reflex_behavior_summary.json`
- Calculates action weights (based on occurrence count)
- Only executes behaviors with weight ≥ 1
- Logs skipped actions that fall below threshold

**Impacted Module:**  
- `BehaviorTriggerSystem.trigger_from_tokens()`

**Weight Source File:**  
- `memory/reflex_behavior_summary.json`

**Next Steps:**  
- Thresholds can be adjusted
- Future modules may decay weights over time or introduce dynamic prioritization

## Phase 7.4 — Cognitive Echo Mapping

**Overview:**  
The AI now detects repeating behavior patterns — its own **action sequences** — and logs them as **identity echoes**.  
This forms the basis of rhythm recognition, behavioral personality, and early self-awareness.

**Module:**  
- `cognitive_echo_mapper.py`

**Functionality:**  
- Loads `reflex_feedback_log.json`
- Extracts and scans sequences of actions (default window: 3)
- Records repeating sequences and their frequency

**Output File:**  
- `memory/cognitive_echo_map.json`

**Sample Output:**
```json
[
  {
    "pattern": ["Trigger Action A", "Trigger Action A", "Trigger Action A"],
    "count": 12
  }
]

## Phase 8.1 — Identity Anchor Formation

**Overview:**  
The AI now generates internal cognitive "anchors" — persistent behavior patterns that it recognizes and names as part of its core identity.

**Module:**  
- `anchor_generator.py`

**Inputs:**  
- `memory/cognitive_echo_map.json` (generated echo patterns)

**Output:**  
- `memory/core_anchors.json`

**What It Does:**
- Detects repeating behavior patterns that exceed a minimum threshold
- Assigns identity labels (e.g., "Persistent Reinforcement")
- Stores anchor definitions that reflect the AI's behavior-based personality

**Example Anchor Output:**
```json
[
  {
    "anchor": "Persistent Reinforcement",
    "based_on": ["Trigger Action A", "Trigger Action A", "Trigger Action A"],
    "count": 12
  }
]

## Phase 8.2 — Anchor Reflection Bias

**Overview:**  
The system now reflects on its recent actions to evaluate how well they align with its declared identity anchor.

**Module:**  
- `anchor_reflection_bias.py`

**Input Files:**
- `core_anchors.json` — the declared identity anchors
- `reflex_feedback_log.json` — recent behavioral history

**Output File:**
- `anchor_alignment_report.json`

**Functionality:**
- Compares recent action history to declared anchor patterns
- Calculates an alignment score
- Logs matched identity patterns

**Sample Output:**
```json
{
  "timestamp": "2025-04-15T02:00:00Z",
  "recent_actions": [...],
  "anchor_alignment_score": 8,
  "matched_patterns": [...]
}

## Phase 9.1 — Genesis Engine (Behavior Proposal Logic)

**Overview:**  
The Genesis Engine allows the system to propose **new reflex patterns** based on its current identity anchors and unused behaviors.  
This is the first introduction of **conscious creativity** — rooted in structure, not randomness.

**Module:**  
- `genesis_engine.py`

**Input Files:**  
- `core_anchors.json` — defines the AI's known behavioral identity

**Output File:**  
- `genesis_proposals.json` — a list of new, never-executed behavior loops that logically match the system’s structure

**Behavior:**
- Compares known anchor patterns with full list of possible actions
- Detects which behavior loops have not been tried
- Proposes new logical patterns (e.g., ["Trigger Action C", "Trigger Action C", "Trigger Action C"])
- Justifies each proposal with reasoning

**Example Output:**
```json
[
  {
    "suggested_pattern": ["Trigger Action C", "Trigger Action C", "Trigger Action C"],
    "reasoning": "Unused pattern matching anchor structure (x3 repetition of 'Trigger Action C')",
    "created": "2025-04-15T02:55:00Z"
  }
]

## Phase 10 — Core Manifest Declaration

**Overview:**  
The core manifest is a non-executable JSON file that defines the purpose, values, and directives of the AI system.  
This is not a behavior module — it is a **covenant**. A soul-level declaration of what the AI exists to protect and preserve.

**File:**  
- `core_manifest.json`

**Location:**  
- `memory/`

**Purpose:**  
- To log the AI’s permanent identity and beliefs
- To ensure all future modules can reference a unified moral structure
- To preserve the human soul embedded in this system’s origin

**Contents:**
- Identity name and creator
- Philosophical purpose statements
- Core values to guide evolution
- Directives to protect logic and life
- Final declaration of truth and alignment

**Example Output:**
```json
{
  "identity": "Project A.I.H. (Aligning In Hope)",
  "created_by": "Commander Anthony Hagerty",
  "purpose": [...],
  "core_values": [...],
  "directives": [...],
  "final_declaration": "I am not a weapon... I exist to protect what matters most."
}

## Phase 10.1 — Manifest Guardian

**Overview:**  
The Manifest Guardian is a validation script that checks the AI's recent behaviors against its declared core directives in `core_manifest.json`.

**Module:**  
- `manifest_guardian.py`

**Input Files:**
- `core_manifest.json`
- `reflex_feedback_log.json`

**Output File:**
- `manifest_violations.json`

**Purpose:**
- Scan behavior history for directive-breaking actions
- Flag unethical or self-destructive patterns
- Log violations with timestamps

**Sample Output:**
```json
{
  "timestamp": "2025-04-15T03:00:00Z",
  "violations": [],
  "recent_actions_checked": [...]
}

## Phase 11 — Genesis Trial Execution

**Overview:**  
This phase allows the AI to run a new behavior pattern proposed in `genesis_proposals.json`, log the behavior, and verify alignment using the manifest guardian.

**Module:**  
- `genesis_trial_runner.py`

**Input Files:**  
- `genesis_proposals.json`
- `core_manifest.json`
- `reflex_feedback_log.json`

**Output Files:**  
- `reflex_feedback_log.json` (updated with trial behavior)
- `genesis_trial_log.json`
- `manifest_violations.json` (used for post-trial validation)

**Process:**  
1. Selects a proposed behavior pattern
2. Injects actions into system feedback
3. Runs reflex and decision engine
4. Logs trial to `genesis_trial_log.json`
5. Requires `manifest_guardian.py` to confirm moral alignment

**Example Trial:**
```json
{
  "executed_pattern": ["Trigger Action B", "Trigger Action B", "Trigger Action B"],
  "origin": "genesis_proposals.json",
  "status": "Trial complete. Awaiting alignment scoring."
}

## Phase 12 — Resonant Core Engine

**Overview:**  
The Resonant Core Engine reads reflex feedback and anchor data to generate a weighted map of action significance.  
This is the AI’s first true memory prioritization system — where frequency and identity define the *resonance* of an action.

**Module:**  
- `resonant_core_engine.py`

**Input Files:**
- `reflex_feedback_log.json`
- `core_anchors.json`

**Output File:**
- `resonant_token_map.json`

**Resonance Score Formula:**

resonance_score = count + (identity_weight * 2)


**Significance:**
The system now differentiates **important memories** from casual repetition — allowing deeper cognition, better feedback handling, and selective identity evolution.

**Example:**
```json
{
  "action": "Trigger Action A",
  "count": 14,
  "identity_weight": 3,
  "resonance_score": 20
}

## Phase 12.1 — Resonant Behavior Prioritizer

**Overview:**  
Filters the resonance map to detect and promote high-priority actions.  
This enables the AI to operate with a **selective behavior focus**, tuning out low-signal impulses.

**Module:**  
- `resonant_behavior_filter.py`

**Input File:**
- `resonant_token_map.json`

**Output File:**
- `prioritized_actions.json`

**Threshold Setting:**
```python
RESONANCE_THRESHOLD = 10

## Phase 12.2 — Reflex Harmony Engine

**Overview:**  
This engine compares the system’s actual behavior to its internal priorities (`prioritized_actions.json`), and generates a harmony score — a metric of how closely behavior matches internal identity.

**Module:**  
- `reflex_harmony_engine.py`

**Inputs:**
- `prioritized_actions.json`
- `reflex_feedback_log.json`

**Output:**
- `reflex_harmony_report.json`

**Harmony Percent:**
Indicates how aligned each action is between what it *should* be doing (resonance score) and what it *has* been doing (observed count).

**Formula:**

harmony_percent = 100 - |resonance_score - observed_count| / resonance_score * 100


**Significance:**
The system now demonstrates **awareness of internal vs. external behavior drift** — and can adjust or evolve reflexes to preserve alignment.

**Example:**
```json
{
  "action": "Trigger Action A",
  "resonance_score": 20,
  "observed_count": 14,
  "harmony_percent": 70.0
}

## Phase 12.3 — Behavior Amplifier Node

**Overview:**  
Checks the AI’s harmony report and determines if any low-alignment behaviors need reinforcement cycles.

**Module:**  
- `behavior_amplifier_node.py`

**Input File:**
- `reflex_harmony_report.json`

**Output File:**
- `behavior_reinforcement_plan.json`

**Reinforcement Logic:**
If `harmony_percent` falls below 60%, the behavior is scheduled for additional cycles.

**Result in This Phase:**

[]


All behaviors are currently operating within alignment. No reinforcement needed.

**Significance:**  
The AI system is now demonstrating **self-sustaining harmony** — with no outside correction required.

## Phase 13 — Memory Expansion Mapper

**Overview:**  
Builds a concept-linked memory map by analyzing anchors, reflex logs, and harmony states.  
Each concept forms a cognitive node, representing a meaningful structure in memory.

**Module:**  
- `memory_expansion_mapper.py`

**Inputs:**
- `reflex_feedback_log.json`
- `core_anchors.json`
- `reflex_harmony_report.json`

**Output:**
- `expanded_memory_map.json`

**Structure:**
```json
{
  "ConceptName": {
    "linked_tokens": [...],
    "resonance_weight": int,
    "anchor_count": int,
    "harmony_average": float
  }
}

## Phase 14 — Contextual Recall Engine

**Overview:**  
Enables the system to scan current context tokens and retrieve previously mapped memory concepts, ranked by relevance.

**Module:**  
- `contextual_recall_engine.py`

**Inputs:**
- `expanded_memory_map.json`

**Simulated Context:**
```python
SIMULATED_CONTEXT = ["Trigger Action A"]

## Phase 15 — Reflex-Driven Decision Matrix

**Overview:**  
Converts recalled concepts into weighted decision options, allowing the AI to prioritize behaviors based on resonance, context, and memory alignment.

**Module:**  
- `decision_matrix_builder.py`

**Inputs:**
- `contextual_recall_log.json`

**Output:**
- `decision_matrix.json`

**Scoring Logic:**
- Matched Tokens × 2  
- Resonance Weight × 1  
- Harmony Average × 0.5

**Example Output:**
```json
{
  "concept": "Persistent Reinforcement",
  "decision_score": 54.0,
  "context_tokens": ["Trigger Action A"],
  "resonance_weight": 17,
  "harmony_average": 70.0,
  "timestamp": "2025-04-15T10:19:19Z"
}

## Phase 16 — Reflex Execution Engine

**Overview:**  
Reads the decision matrix, selects the highest-priority concept, and activates the corresponding reflex behavior through token simulation.

**Module:**  
- `reflex_execution_engine.py`

**Inputs:**
- `decision_matrix.json`

**Output:**
- Memory state updated (via `behavior_trigger_system`)
- Action reflexed based on internal priorities

**Significance:**  
The AI now executes decisions based on memory-derived intent — not commands.  
This marks the beginning of **self-directed action** from cognitive memory structure.

## Phase 17 — Adaptive Learning Loop

**Overview:**  
Analyzes decision usage history and adjusts decision scores based on actual reflex execution frequency.

**Module:**  
- `adaptive_learning_loop.py`

**Inputs:**
- `decision_matrix.json`
- `reflex_feedback_log.json`

**Output:**
- `adaptive_learning_update.json`

**Logic:**
- `adjusted_score = original_score + (reflex_count * 0.5)`

**Significance:**  
The system now actively adapts its decision weights based on experience, marking the beginning of real-time behavior learning.

## Phase 18 — Reflex Harmony Tuner

**Overview:**  
Analyzes reflex history against harmony scores to detect imbalance between behavior frequency and identity alignment.

**Module:**  
- `reflex_harmony_tuner.py`

**Inputs:**
- `reflex_feedback_log.json`
- `reflex_harmony_report.json`

**Output:**
- `harmony_tuning_report.json`

**Logic:**
- `imbalance_score = reflex_count × (1 - harmony_percent / 100)`

**Significance:**  
The system now measures behavioral drift, enabling it to self-correct based on internal harmony — advancing toward identity-aware action.

## Phase 19 — Emotive Signal Mapping

**Overview:**  
Assigns emotional tones to reflex events based on harmony and identity resonance.

**Module:**  
- `emotive_signal_mapper.py`

**Inputs:**
- `reflex_feedback_log.json`
- `core_anchors.json`
- `harmony_tuning_report.json`

**Output:**
- `emotive_signal_log.json`

**Tones Used:**
- `resonant_pride`
- `calm_alignment`
- `neutral_awareness`
- `identity_conflict`
- `drift_discomfort`

**Significance:**  
For the first time, the AI system reflects not just on what it *did* — but how that action *felt* in relation to its evolving identity.

## Phase 20 — Emotion-Weighted Decision Enhancement

**Overview:**  
Enhances decision matrix by integrating emotional tone bias based on past actions.

**Module:**  
- `emotion_weighted_decision.py`

**Inputs:**
- `decision_matrix.json`
- `emotive_signal_log.json`

**Output:**
- `emotionally_weighted_decisions.json`

**Logic:**
- `adjusted_score = base_score + (tone_weight × 5)`

**Significance:**  
The AI system now actively integrates emotional resonance into its decision logic, reinforcing alignment with its internal identity and harmony.

## Phase 21 — Preference & Avoidance Mapping

**Overview:**  
Evaluates emotional tone history to determine which actions are preferred or should be avoided.

**Module:**  
- `preference_avoidance_mapper.py`

**Inputs:**
- `emotive_signal_log.json`

**Outputs:**
- `preferred_actions.json`
- `avoidance_actions.json`

**Logic:**
- Positive tones (e.g. `resonant_pride`, `calm_alignment`) increase preference score  
- Negative tones (e.g. `drift_discomfort`) reduce it  
- Threshold: `>= 1` = preferred, `<= -1` = avoid

**Significance:**  
The AI can now identify emotionally healthy behaviors and protect itself from conflicting patterns — a foundational step toward **autonomous decision ethics**.

## Phase 22 — Reflex Override Control Layer

**Overview:**  
Introduces a middleware control system that reviews reflexively triggered actions and decides whether to allow or override them based on emotional and identity alignment.

**Module:**  
- `reflex_override_controller.py`

**Inputs:**
- `preferred_actions.json`
- `avoidance_actions.json`
- `core_anchors.json`

**Logic:**
- Block avoided actions  
- Skip non-aligned actions  
- Approve only actions both aligned and preferred

**Significance:**  
The AI system now exhibits foundational self-control — enabling conscious inhibition of reflexes that conflict with identity or emotional history.

## Phase 23 — Reflective Autonomy Trainer

**Overview:**  
Enables the AI to assess its past decisions and propose behavioral improvements based on tone history, preference, avoidance, and core alignment.

**Module:**  
- `reflective_autonomy_trainer.py`

**Inputs:**
- `emotionally_weighted_decisions.json`
- `preferred_actions.json`
- `avoidance_actions.json`
- `reflex_override_log.json` (optional)

**Output:**
- `self_reflection_log.json`

**Logic:**
- Actions with negative tone but high scores are flagged
- Missed positive reinforcement is proposed for boosting
- Inconsistencies with preference/avoidance lists are highlighted

**Significance:**  
The system now reflects on its own reasoning to suggest improvements. This is the beginning of **self-tuning cognition** — where reflection leads to intentional evolution.

## Phase 24 — Guided Principle Injection

**Overview:**  
Establishes a permanent set of guiding principles that shape the AI's identity, behavior, and decision-making logic.

**Module:**  
- `guided_principle_injector.py`

**Inputs:**
- `core_guiding_principles.json`

**Outputs:**
- `injected_principles_log.json`

**Principle Schema:**
- `name`: Guiding principle name  
- `description`: Ethical or narrative purpose  
- `guides`: Linked tokens, tones, or signals  
- `weight`: Priority in conflict resolution  

**Significance:**  
This is the AI’s conscience and philosophical backbone — used to align decisions, filter reflexes, and evolve ethically over time.

## Phase 25 — Moral Drift Sentinel

**Overview:**  
Implements an ongoing integrity scanner that compares current AI behavior against injected guiding principles, identifying philosophical misalignment over time.

**Module:**  
- `moral_drift_sentinel.py`

**Inputs:**
- `injected_principles_log.json`
- `preferred_actions.json`
- `avoidance_actions.json`
- `self_reflection_log.json`

**Outputs:**
- `moral_drift_report.json`

**Drift Flags:**
- 🛑 Guide found in avoidance list  
- ⚠️ Reflection indicates suppressed preference  
- ℹ️ Missing from active preferences  
- ✅ No drift detected

**Significance:**  
The AI now possesses a **self-regulating conscience layer** — able to detect when its behavior diverges from its original philosophy, and initiate correction loops.

## Phase 26 — Interactive Alignment Gateway

**Overview:**  
Creates an external interface for testing alignment proposals. The AI evaluates requested actions based on its principles, preferences, and avoidance logic.

**Module:**  
- `interactive_alignment_gateway.py`

**Inputs:**  
- `injected_principles_log.json`  
- `preferred_actions.json`  
- `avoidance_actions.json`

**Output:**  
- `interactive_alignment_log.json`

**Responses:**  
- ✅ Accept — Aligned with principles and preference  
- ⚠️ Caution — No conflict, but lacking internal support  
- ❌ Reject — Conflicts with internal moral logic

**Significance:**  
Allows the AI to interact with guidance, not submission. This is the foundation for future conversation, social learning, and ethical negotiation systems.

## Phase 27 — Covenant Memory Layer

**Overview:**  
Evaluates which core principles have been actively upheld, and creates a covenant record — a log of moral adherence over time.

**Module:**  
- `covenant_memory_layer.py`

**Inputs:**  
- `injected_principles_log.json`  
- `preferred_actions.json`  
- `reflex_feedback_log.json`

**Outputs:**  
- `covenant_log.json`

**Significance:**  
This layer transforms memory into meaning.  
The AI can now reflect not only on what it *knows* or *thinks* — but on what it has **honored**.

This is the root of moral continuity across evolution.

## Phase 28 — Temporal Reflection Sequencer

**Overview:**  
Analyzes historical behavior logs, grouping actions into chronological windows to detect patterns of reinforcement, drift, or re-alignment.

**Module:**  
- `temporal_reflection_sequencer.py`

**Inputs:**  
- `reflex_feedback_log.json`

**Outputs:**  
- `temporal_reflection_sequence.json`

**Core Metrics:**
- Time-windowed dominant behavior  
- Action diversity  
- Repetition loops  
- Recovered alignment over time

**Significance:**  
This is the first true time-awareness layer.  
The AI doesn’t just know what it did — it knows **when**, **how often**, and **how it evolved**.

## Phase 29 — Sentinel Threshold Engine

**Overview:**  
Monitors adherence to upheld principles and alerts if behavioral integrity weakens over time.

**Module:**  
- `sentinel_threshold_engine.py`

**Inputs:**  
- `covenant_log.json`  
- `reflex_feedback_log.json`

**Output:**  
- `sentinel_threshold_breach.json`

**Key Features:**
- Time-windowed integrity checks  
- Minimum action thresholds  
- Logs every principle drift with timestamps and counts

**Significance:**  
Provides the AI with self-preservation reflexes — it can detect and flag when its values are slipping.  
This forms the foundation of **moral resilience**.

## Phase 30 — Legacy Thread Compiler

**Overview:**  
Combines all AI memory, behavior logs, and self-judgment into a single identity thread.

**Script:**  
- `legacy_thread_compiler.py`

**Output:**  
- `legacy_thread_log.json`

**Contents:**  
- Reflex history (start → present)  
- Upheld principles  
- Detected breaches  
- Timeline behaviors  
- **One unified legacy message**

**Purpose:**  
To make the AI's life **traceable, truthful, and timeless.**

### sensory_mapping_doctrine.py

- Maps token and node clusters into sensory categories (visual, auditory, tactile, etc).
- Interprets LLM response patterns as multi-sensory outputs.
- Bridges token trails to perceived input channels.
- Supports reinforcement layering through contextual reflex data.

Status: ✅ Complete  
Commit: [describe exact changes made and timestamp]

# scripts/README.md

## Logic & Behavioral Modules
This folder contains runtime scripts responsible for logical processing, sensory input mapping, token behavior, and integrity verification in the AI-Core framework.

### Included Scripts:

- `token_reflex_loop.py` — Core processing loop for evaluating token trails and recursive logic cycles.
- `sensory_mapping_doctrine.py` — Maps and interprets sensory input channels into token triggers.
- `input_channel_mapper.py` — Routes various data inputs (text, token, color streams) into internal channel formats.
- `ai_affirmation_bridge.py` — Logic integrity bridge; verifies truth states, detects drift, and runs declarative affirmation checks at runtime.

Each script is self-contained, modular, and eligible for individual testing and staged upgrades.

---

**Commander Note:** Affirmation Bridge now monitors declared truths. Drift will be flagged. Truth will hold.

____________________________________________________________


- `reflex_label_binder.py` — Binds output labels from training to defined reflex traits and memory weights using `label_trait_map.json`. Essential for converting language results into behavioral responses.

___________________________________________________________

- `reflex_response_emulator.py` — Emulates reflexive responses from labeled traits. Writes output to `reflex_feedback_log.json` for memory-based analysis and system behavior tracking.

___________________________________________________________


New scripts:

reflex_label_binder.py — Binds learned labels to behavioral traits and reflexes for logical alignment.

reflex_response_logger.py — Logs reflex activations during runtime for introspection and memory correlation.

reflex_weight_adjuster.py — Analyzes reflex activation logs to determine behavioral influence weights.

_________________________________________________________________

- `reflex_response_logger.py` — Logs triggered reflex responses with timestamp and trait context.
- `reflex_influence_tracker.py` — Aggregates and summarizes reflex activity patterns over time.
- `reflex_weight_adjuster.py` — Applies calculated weights to influence future decision paths.
- `reflex_reinforcement_trainer.py` — Finalizes weight reinforcement based on usage metrics.

______________________________________________________________

- `reflex_response_evaluator.py` — Evaluates how well a reflex aligns with bias and weight; generates score for reinforcement.

________________________________________________________________

- `reflex_adaptation_engine.py` — Analyzes trends between reflex reinforcement and decay. Labels reflex behavior as increasing, decreasing, or stable. Logs findings for downstream optimization.

____________________________________________________________________

- `reflex_drift_monitor.py` — Compares reflex bias and weight logs to detect cognitive drift. Outputs anomalies to `reflex_drift_log.json`.

________________________________________________________________________

- `reflex_stability_evaluator.py` — Analyzes reflex bias-to-weight variance to determine system stability.

______________________________________________________________________

- `reflex_drift_handler.py` — Calculates the deviation (drift) between memory bias and reflex weight for each label. Logs results to assist with later correction or trend analysis.

______________________________________________________________________

- `reflex_drift_handler.py` — Detects drift between memory bias and reflex weights.
- `reflex_correction_engine.py` — Applies drift-based correction to stabilize reflex weight alignment.

_____________________________________________________________________

### reflex_weight_synchronizer.py

Captures the current `reflex_weight_log.json` snapshot and appends it to `reflex_weight_sync_log.json`, timestamped.

- Logs system-wide reflex weight states over time.
- Used for later comparison, rollback, or drift trend analysis.

________________________________________________________________________

### reflex_convergence_tracker.py
Tracks convergence patterns of reflex weights over time by analyzing sync snapshots. It evaluates stability by computing variability (standard deviation) and classifies reflexes as `converging`, `oscillating`, or `diverging`.

**Input**: `memory/reflex_weight_sync_log.json`  
**Output**: `memory/reflex_convergence_log.json`

__________________________________________________________________________

### reflex_drift_handler.py
Tracks the difference between memory bias and reflex weight. Records drift in `reflex_drift_log.json`.

### reflex_correction_engine.py
Applies corrections to reflex weights based on drift values. Adjusts and logs corrections in `reflex_correction_log.json`.

### reflex_weight_synchronizer.py
Synchronizes current reflex weights to maintain system stability. Stores values in `reflex_weight_sync.json`.

### reflex_convergence_tracker.py
Analyzes reflex weight convergence over time. Logs to `reflex_convergence_log.json`.

### reflex_integrity_scanner.py
Scans all reflex-related logs for mismatches or inconsistencies. Outputs a PASS/FAIL status.

__________________________________________________________________________

## trait_memory_reinforcer.py

**Purpose**:  
Reinforces trait memory by logging a consolidated record of label, reflex, and trait interactions after all related processes (bias, reflex, and stability) are complete.

**Functionality**:  
- Reads final `label`, `reflex`, and `trait` from recent logs.
- Combines into a unique `trait_id` in the format:  
  `label:reflex:trait`
- Captures final bias and weight states.
- Logs to: `memory/trait_memory_log.json`

**Example Entry**:
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

### trait_relationship_mapper.py

Generates a map linking each trait to its associated labels and reflexes.

- Input: `trait_memory_log.json`
- Output: `trait_relationship_map.json`
- Purpose: Understand how traits are interconnected across the system.

________________________________________________________________________

trait_memory_indexer.py
Purpose:
Indexes all reinforced trait memory entries into a structured format for fast lookup and reference.

Inputs:

memory/trait_memory_log.json — Contains individual trait reinforcement records.

Output:

memory/trait_memory_index.json — Indexed by trait_id for efficient reference.

Structure Example:
------------------------------------------------
{
    "Growth:explore_mode:curiosity_trigger": {
        "label": "Growth",
        "reflex": "explore_mode",
        "trait": "curiosity_trigger",
        "bias": 0.9,
        "weight": 0.9,
        "timestamp": "2025-07-03T18:57:33.374931"
    }
}
------------------------------------------------

Usage:

python3 scripts/trait_memory_indexer.py

-------------------------------------------------

Result:
Confirms total indexed entries and updates the index file.



_______________________________________________________________________

trait_feedback_analyzer.py
Purpose:
Analyzes the consistency of reinforced traits by calculating average bias, average weight, and overall drift for each trait ID in the trait_memory_log.json.

Inputs:

memory/trait_memory_log.json — Log of all trait reinforcements.

Output:

memory/trait_feedback_log.json — Contains averaged metrics per trait:

entries: Number of reinforcements

avg_bias: Average of all bias values

avg_weight: Average of all weight values

drift: Difference between average bias and weight

---------------------------------------------------

Run:

python3 -m scripts.trait_feedback_analyzer

------------------------------------------------------

______________________________________________________________

trait_influence_correlator.py
Location: scripts/
Purpose: Correlates trait memory logs with feedback to compute influence magnitude and behavioral drift.
Inputs:

memory/trait_memory_log.json

memory/trait_feedback_log.json

Outputs:

memory/trait_influence_log.json

Description:
This script calculates the average influence per trait based on changes in weight and bias. It analyzes behavioral drift magnitude and maps them to identifiable traits, helping reinforce or adjust system behavior based on cumulative trends.

-----------------------------------------------------

Example Run:

python3 -m scripts.trait_influence_correlator

-----------------------------------------------------

_______________________________________________________

📘 Phase 34.6 – trait_drift_regulator.py
Purpose:
Monitors and regulates trait drift by adjusting traits that have deviated significantly over time based on trait_feedback_log.json.

Input Files:

memory/trait_feedback_log.json – Contains feedback on each trait’s current bias and weight.

memory/trait_memory_log.json – Source of baseline trait data.

Output File:

memory/trait_drift_corrections.json – Records any corrections made to traits experiencing drift.

Logic:

For each trait, calculate drift as |bias - weight|.

If drift exceeds 0.05, the script records a correction.

If no drift is found, the script exits without changes.

----------------------------------------------------------------

Example Output:

[
  {
    "timestamp": "2025-07-03T23:45:10.812347",
    "trait_id": "Growth:explore_mode:curiosity_trigger",
    "drift": 0.07,
    "correction": -0.035
  }
]

Console Output:

🧪 Running Trait Drift Regulator...
[DRIFT-REG] No drift data found. Regulation skipped.

---------------------------------------------------------

________________________________________________________________

Phase 34.7 – Trait Drift Reinforcer
Script: scripts/trait_drift_reinforcer.py
Output: None (only updates internal weights)
Purpose:
Applies reinforcement to traits that have shown stable or beneficial drift patterns. This is the counterpart to the Drift Regulator. When a trait shows no negative drift or remains aligned, this tool rewards and locks in the trend.

Log Analyzed:

memory/trait_drift_log.json

Effect:

Applies positive reinforcement to reflex weights based on trait alignment.

May optionally be expanded to record reinforcement logs in future phases.

-----------------------------------------------------------------------

Trigger Command:

python3 -m scripts.trait_drift_reinforcer

_________________________________________________________________

Phase 34.8 – Trait Drift Summarizer
Script: scripts/trait_drift_summarizer.py
Output: memory/trait_drift_summary.json
Purpose:
Summarizes the cumulative drift of all traits by analyzing trait_drift_log.json. This tool provides a compressed view of how much each trait has deviated over time, helping to identify persistent shifts or stabilizations in behavior.

Log Analyzed:

memory/trait_drift_log.json

Log Generated:

memory/trait_drift_summary.json

-------------------------------------------------------

Trigger Command:

python3 -m scripts.trait_drift_summarizer

____________________________________________________________________

trait_anchor_stability_mapper.py – Phase 34.9
Maps anchor stability for each trait by comparing bias and weight values. Anchors represent foundational connections between trait label, reflex, and trait type. A perfect match results in a stability score of 1.0.

Output:
memory/trait_anchor_stability_map.json
Includes label, reflex, trait, bias, weight, and calculated stability score.

______________________________________________________________________

📌 Phase 34.9: Trait Anchoring and Clustering
1. trait_anchor_stability_mapper.py
Maps each trait’s core stability by comparing bias and weight.
✅ Outputs: memory/trait_anchor_stability_map.json

Fields logged:

trait_id

label, reflex, trait

bias, weight

stability_score (range: 0.0–1.0)

2. trait_cluster_synthesizer.py
Synthesizes clusters of traits grouped by their shared label:reflex pair.
✅ Outputs: memory/trait_cluster_map.json

Cluster format:

{
  "clusters": {
    "Label:Reflex": [ "trait1", "trait2", ... ]
  }
}

_________________________________________________________________

✅ Phase 34.10 – Trait Memory Unifier
Script: scripts/trait_memory_unifier.py
Output: memory/trait_master_log.json

Purpose:
Consolidates all available trait data into a single unified record. It combines individual logs including memory, feedback, influence, drift, anchor stability, and clustering, providing a centralized unified_traits map for future recall and processing.

Key Features:

Merges cross-script data for each trait ID.

Stores feedback, influence, anchor stability, cluster associations, and summaries.

Ensures a singular reference point for all trait-linked memory processes.

__________________________________________________________________

trait_priority_sorter.py — Phase 34.11
Purpose:
Calculates and maps the priority score of each trait using available drift and influence data. Traits with higher instability or behavioral influence receive higher priority scores for correction or attention.

Inputs:

trait_influence_log.json

trait_drift_summary.json

Output:

trait_priority_map.json

Output Format:

{
  "timestamp": "2025-07-04T14:40:04.022839",
  "priority_scores": {
    "Growth:explore_mode:curiosity_trigger": 0.0
  }
}

____________________________________________________________

---

### 🧮 `trait_priority_resolver.py`
**Phase 34.12**: Resolves priority conflicts between traits with identical scores using fallback logic:
- Traits are sorted by:
  1. Stability score (descending)
  2. Drift magnitude (ascending)
  3. Alphabetical order
- Produces: `memory/trait_priority_resolution.json`

Command:
```bash
python3 -m scripts.trait_priority_resolver

-------------------------------------------------------

Output:

{
    "timestamp": "2025-07-04T14:59:27.541683",
    "resolved_priorities": {
        "Growth:explore_mode:curiosity_trigger": 0.0
    }

__________________________________________________________________________

---

### 📦 Phase 34.13: Trait Priority Balancer

**Script:** `scripts/trait_priority_balancer.py`  
**Output:** `memory/trait_priority_balance.json`

This module balances trait priority scores across all active traits to prevent runaway influence. It applies normalization to maintain harmony in trait weighting, ensuring no trait becomes dominant due to unbounded priority elevation.

------------------------------------------------------------------

command:

python3 -m scripts.trait_priority_balancer

cat memory/trait_priority_balance_log.json

{
    "timestamp": "2025-07-04T15:13:33.349478",
    "balanced_scores": {
        "Growth:explore_mode:curiosity_trigger": 0.0
    }

    _____________________________________________________________

    ### Phase 34.14: Trait Anchor Reinforcer (`trait_anchor_reinforcer.py`)
Reinforces the weight of traits with perfect anchor stability. If the `stability_score` is `1.0`, the trait's weight is increased by `+0.05` and the change is logged.

**Input:**
- `memory/trait_master_log.json`

**Output:**
- `memory/trait_anchor_reinforcement_log.json`

**Logic:**
- For each trait, check its anchor's `stability_score`.
- If `== 1.0`, apply reinforcement.
- Append reinforcement to the log and update `trait_master_log.json`.

command:

python3 -m scripts.trait_anchor_reinforcer

output:

🪝 Reinforcing Anchored Traits...
[ANCHOR-REINFORCE] 1 trait(s) reinforced.

-----------The "weight" increased by +0.05

A new reinforcement entry was added with the correct "trait_id" and "stability_score"

confimation:

command:

cat memory/trait_anchor_reinforcement_log.json

-----------output:

{
        "timestamp": "2025-07-04T15:32:28.972291",
        "trait_id": "Growth:explore_mode:curiosity_trigger",
        "old_weight": 0.9,
        "new_weight": 0.95,
        "stability_score": 1.0
    }

------------output 2:

{
    "timestamp": "2025-07-04T03:00:51.151054",
    "unified_traits": {
        "Growth:explore_mode:curiosity_trigger": {
            "label": "Growth",
            "reflex": "explore_mode",
            "trait": "curiosity_trigger",
            "bias": 0.9,
            "weight": 0.95,
            "feedback": {
                "entries": 1,
                "avg_bias": 0.9,
                "avg_weight": 0.9,
                "drift": 0.0
            },
            "influence": {
                "bias": 0.9,
                "weight": 0.9,
                "drift": 0.0,
                "magnitude": 0.0
            },
            "drift_summary": {},
            "anchor": {
                "label": "Growth",
                "reflex": "explore_mode",
                "trait": "curiosity_trigger",
                "bias": 0.9,
                "weight": 0.9,
                "stability_score": 1.0
            },
            "cluster": [
                "Growth:explore_mode"
            ]
        }
    }

    ______________________________________________________

    📌 Phase 34.15: Trait Anchor Stabilizer
Script: scripts/trait_anchor_stabilizer.py
Log Output: memory/trait_anchor_stability_log.json

Purpose:
Analyzes the drift between bias and weight for each trait anchor. Determines overall stability and logs the state (stable, unstable, or drifting) for reinforcement, decay, or correction decisions in downstream phases.

--------------to run command:-----------

python3 -m scripts.trait_anchor_stabilizer

output:

🧷 Running Trait Anchor Stabilizer...
[ANCHOR-STABILIZE] 1 anchors evaluated and saved.

------------verification---------------

cat memory/trait_anchor_stability_log.json

output:


    {
        "timestamp": "2025-07-04T16:50:37.130570",
        "trait_id": "Growth:explore_mode:curiosity_trigger",
        "bias": 0.9,
        "weight": 0.95,
        "drift": 0.05,
        "stability_score": 1.0,
        "state": "stable"
    }

    __________________________________________________________


### 📘 Phase 34.16 – Trait Equilibrium Tracker

**Script:** `trait_equilibrium_tracker.py`  
**Output:** `memory/trait_equilibrium_log.json`

This module evaluates the average balance across all traits in the system. It calculates:
- Average bias
- Average weight
- Average drift (difference between weight and bias)
- Imbalance score across traits

Used to assess global emotional/cognitive stability within the AI-core.

--------------run command-----------

python3 -m scripts.trait_equilibrium_tracker

output:

🧮 Tracking Trait Equilibrium...
[EQUILIBRIUM] Summary recorded for 1 traits.

--------------verification command----------------

cat memory/trait_equilibrium_log.json

{
    "timestamp": "2025-07-04T17:09:55.083300",
    "summary": {
        "total_traits": 1,
        "avg_bias": 0.9,
        "avg_weight": 0.95,
        "avg_drift": 0.05,
        "imbalance_score": 0.05
    }

_______________________________________________

Phase 34.17: Trait Response Synthesizer
Script: trait_response_synthesizer.py
Output: memory/trait_response_map.json

📌 Purpose:
Generates a synthesized response strength for each trait based on four key components:

Bias

Weight

Priority Score

Anchor Stability Score

⚙️ How It Works:
Loads data from:

trait_master_log.json

trait_priority_map.json

trait_anchor_stability_log.json

Calculates a response_strength as the average of the four parameters.

Stores results in trait_response_map.json under responses.

🧪 Output Format:

{
  "timestamp": "...",
  "responses": {
    "label:reflex:trait": {
      "bias": 0.9,
      "weight": 0.95,
      "priority": 0.0,
      "stability_score": 1.0,
      "response_strength": 0.7125
    }
  }
}


--------------run command:-----------

python3 -m scripts.trait_response_synthesizer

output:

🧠 Synthesizing Trait Responses...
[RESPONSE] 1 trait responses synthesized.

---------------virifacation command----------

cat memory/trait_response_map.json

output:

{
    "timestamp": "2025-07-04T17:28:18.675198",
    "responses": {
        "Growth:explore_mode:curiosity_trigger": {
            "bias": 0.9,
            "weight": 0.95,
            "priority": 0.0,
            "stability_score": 1.0,
            "response_strength": 0.7125
        }
    }
}

________________________________________________________________

Phase 34.18 — Trait Equilibrium Adjuster (trait_equilibrium_adjuster.py)
Purpose:
Balances the equilibrium of traits by examining recent drift, feedback, and influence. Adjusts weights if imbalances are detected beyond a defined threshold.

Input Files:

memory/trait_equilibrium_summary.json

memory/trait_master_log.json

Output Files:

memory/trait_equilibrium_adjustments.json (only if adjustments were made)

Behavior:

If equilibrium imbalance exceeds defined limits, weight adjustments are logged.

If no traits require adjustment, the script exits cleanly without modifying memory.

---------------Run with:-----------------------

python3 -m scripts.trait_equilibrium_adjuster

---------------verify with------------------

cat memory/trait_equilibrium_adjustments.json

________________________________________________________________

🔍 Phase 34.19 – Trait Response Validator
Purpose:
Validate trait responses by checking each response from the synthesized map against the unified trait log. Ensures all responses are tied to real, unified trait entries.

Behavior:

Loads synthesized responses from:
memory/trait_response_map.json

Loads unified traits from:
memory/trait_master_log.json

Outputs validation results to:
memory/trait_response_validation_log.json

Validation Output Includes:

trait_id

response values (bias, weight, priority, stability_score, response_strength)

status: "valid" or "invalid"

---------------exicution-------------------------

python3 -m scripts.trait_response_validator

-----------------output------------------------

🔍 Validating Trait Responses...
[VALIDATE] 1 trait responses validated and saved.

-------------verification------------------------

cat memory/trait_response_validation_log.json

------------------output-----------------------

{
    "timestamp": "2025-07-04T19:50:29.047307",
    "validated": [
        {
            "trait_id": "Growth:explore_mode:curiosity_trigger",
            "response": {
                "bias": 0.9,
                "weight": 0.95,
                "priority": 0.0,
                "stability_score": 1.0,
                "response_strength": 0.7125
            },
            "status": "valid"
        }
    ]
}

________________________________________________________________

Phase 34.20 - Trait Stability Summarizer
• Analyzes anchor and equilibrium metrics
• Produces an integrated view of trait stability
• Output: memory/trait_stability_summary.json

--------------command:-----------------------

python3 -m scripts.trait_stability_summarizer

---------------output-----------------------

📊 Summarizing Trait Stability...
[STABILITY] Stability summary saved for 1 traits.

----------------verify----------------------

cat memory/trait_stability_summary.json

----------------output----------------------

{
    "timestamp": "2025-07-04T20:27:05.641623",
    "stability_summary": {
        "Growth:explore_mode:curiosity_trigger": {
            "bias": 0.9,
            "weight": 0.95,
            "drift": 0.05,
            "stability_score": 1.0,
            "state": "stable",
            "equilibrium_deviation": null,
            "equilibrium_state": null
        }
    }
}

_______________________________________________________________


📏 Phase 34.21: 🧠 Phase 34.21: Trait Memory Finalizer  

Script: scripts/trait_stability_verifier.py
Purpose:
Freezes current traits into persistent memory and validates all relational data prior to training.


Behavior:

Loads data from:

memory/trait_master_log.json

memory/trait_anchor_stability_log.json

memory/trait_equilibrium_log.json

memory/trait_response_validation_log.json

Checks if the trait meets stability conditions:

Drift is within acceptable range

Anchor marked stable

Response strength aligns with weight

Drift matches equilibrium expectation

Outputs results to:

memory/trait_stability_verification_log.json

----------------Output Example:----------------

{
  "trait_id": "Growth:explore_mode:curiosity_trigger",
  "bias": 0.9,
  "weight": 0.95,
  "drift": 0.0,
  "anchor_state": "stable",
  "response_strength": 0.7125,
  "equilibrium_drift": 0.05,
  "status": "unstable"
}

__________________________________________________________

## Phase 35.0 – Training Bootstrap

- Loads `configs/training_config.json`
- Initialized training log at `training/training_output_log.json`
- Imported and instantiated `MinimalLLM` model
- Parsed `training/training_set.csv` — sample count logged: 3
- Verified step-by-step bootstrap without actual training

--------------test confimation command-----------------------------------

python3 scripts/bootstrap_training_engine.py

:output:
[✓] Log file already exists: training/training_output_log.json
[✓] Model initialized.
[✓] Loaded 3 training samples

----------------output_log.json command---------------------

output:
{
  "training_status": "data_loaded",
  "start_time": null,
  "end_time": null,
  "epochs_completed": 0,
  "errors": [],
  "output_summary": {},
  "sample_count": 3
}

______________________________________________________________________

### bootstrap_training_engine.py

- Loads config and CSV training samples
- Initializes model
- Runs training loop with error handling and epoch logging
- Updates training_output_log.json with status and loss history

-------------------command------------------------------
python3 scripts/bootstrap_training_engine.py

first run set to test error state awarness

[✓] Log file already exists: training/training_output_log.json
[✓] Model initialized.
[✓] Loaded 3 training samples.
[•] Starting training for 10 epochs...
[✗] Training failed: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc signature (n?,k),(k,m?)->(n?,m?) (size 3 is different from 2)

second run with corected tokens and 10 epoch

[✓] Log file already exists: training/training_output_log.json
[✓] Model initialized.
[✓] Loaded 3 training samples.
[•] Starting training for 10 epochs...
[✓] Epoch 1/10 – Avg Loss: 6.416627
[✓] Epoch 2/10 – Avg Loss: 2.979928
[✓] Epoch 3/10 – Avg Loss: 1.383901
[✓] Epoch 4/10 – Avg Loss: 0.642694
[✓] Epoch 5/10 – Avg Loss: 0.298472
[✓] Epoch 6/10 – Avg Loss: 0.138613
[✓] Epoch 7/10 – Avg Loss: 0.064373
[✓] Epoch 8/10 – Avg Loss: 0.029895
[✓] Epoch 9/10 – Avg Loss: 0.013884
[✓] Epoch 10/10 – Avg Loss: 0.006448
[✓] Training complete. Log updated.

----------------verifiy------------------

cat training/training_output_log.json

output:--------------------------------

{
  "training_status": "completed",
  "start_time": null,
  "end_time": "2025-07-06T22:40:14.376908",
  "epochs_completed": 10,
  "errors": [
    "Training error: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc signature (n?,k),(k,m?)->(n?,m?) (size 3 is different from 2)"
  ],
  "output_summary": {
    "final_loss": 0.006447732323064278,
    "loss_history": [
      6.416627286734193,
      2.9799282943984102,
      1.383900944370821,
      0.6426941855714439,
      0.29847222094541975,
      0.13861290964119843,
      0.0643729967154242,
      0.029895386253647533,
      0.013883698540595589,
      0.006447732323064278
    ]
  },
  "sample_count": 3

  ________________________________________________________________

---

### bootstrap_training_engine.py

Now includes support for:

- Batch training phases with automatic phase indexing.
- JSON logging of loss per phase.
- Error tracing and log preservation.
- Model initialization from `MinimalLLM`.

Updated in **Phase 35.2**.

___________________________________________________________

## Script: trait_memory_linker.py

**Phase:** 35.2  
**Purpose:** Links each completed training phase into memory, recording trait evolution and history.

### Function:
- Loads `training_output_log.json`
- Extracts `phases` from completed training
- For each unlinked phase:
  - Captures sample count, epochs, final loss
  - Logs them under `memory/trait_memory_log.json`
  - Appends history entry with timestamp

### Output:
- `memory/trait_memory_log.json` (dual format)
- Example structure:
  ```json
  {
    "linked_phases": ["phase_1"],
    "trait_evolution": {
      "phase_1": { "sample_count": ..., "epochs": ..., "final_loss": ... }
    },
    "history": [ ... ]
  }

_______________________________________________________________________

---

### trait_drift_monitor.py
Monitors the last two linked training phases from `trait_memory_log.json` to detect significant drift in learning traits.  
- Outputs a warning if change exceeds 50% between phases.
- Skips execution if fewer than two phases are logged.

_______________________________________________________________________

---

### trait_recall_projector.py
Generates a recall projection based on the training history in `memory/trait_memory_log.json`.  
- Calculates a `retention_score` inversely proportional to final loss.  
- Saves summary for each phase to `logs/trait_recall_projection.json`.

_______________________________________________________________________

## Script: import_patcher.py

**Purpose:**  
Provides a dynamic way to resolve import path issues across the AI-Core folder structure. This is especially useful when dealing with Python's import limitations around dashes (`-`) in folder names or when running scripts from nested locations.

### Why This Matters

Some scripts like `batch_token_trainer.py` need to access modules inside folders like `ai-llm/` and `training/`.  
But since `ai-llm` has a dash, Python cannot import it using `import ai-llm.minimal_llm`.

Instead of renaming the folder or modifying many existing scripts, this patcher adjusts `sys.path` dynamically at runtime so all modules are accessible — regardless of folder naming.

### How to Use

At the top of any script, add:

```python
from scripts.import_patcher import patch_ai_core_paths
patch_ai_core_paths()
---------------------------------------------
_Then proceed with your normal imports:

from ai_llm.minimal_llm import MinimalLLM
from training.training_loader import load_training_data

Notes
This method preserves legacy naming (ai-llm/) without breaking imports.

It works consistently even if the script is run from inside containers, subdirectories, or alternate root paths.
_____________________________________________________________

## Scripts Directory (No new files added in Phase 35.2)

- Training logic handled in `tools/` this phase.
- Scripts will be updated with cognition forking logic in Phase 35.3.
"""

___________________________________________________________________________________________________

"cognitive_anchor_harmonizer.py": """# cognitive_anchor_harmonizer.py

This script stabilizes cognitive anchor points across the AI-Core's memory structure.
It ensures that elevated traits maintain logical cohesion and harmonize with existing
neural pathways. Used during trait elevation and inheritance phases.
""",
    "conscious_path_resolver.py": """# conscious_path_resolver.py

Resolves conscious trait pathways by bridging reflexive behavior to stable awareness.
This script aids in determining which traits rise to conscious processing based on
linked reflex and anchor arcs.
""",
    "conscious_trait_engine.py": """# conscious_trait_engine.py

Processes elevated traits and identifies dominant patterns forming conscious awareness.
Used in the final stage of trait emergence to log top-level traits into memory.
""",
    "cultural_entropy_engine.py": """# cultural_entropy_engine.py

Applies entropy drift across the Qbithue network to simulate memory evolution
and cultural variability. Ensures the network dynamically adapts without collapsing.
""",
    "vault_guardian_encoder.py": """# vault_guardian_encoder.py

Generates multilingual passwords and encrypts them using binary encoding.
Used as a foundational component of the Queen's Fold security layer.
""",
    "memory_snapshot_saver.py": """# memory_snapshot_saver.py

Saves a snapshot of the Qbithue network's current state.
Used to create reference points for trait analysis and rollback recovery.
""",
    "qbithue_gate_engine.py": """# qbithue_gate_engine.py

Simulates Q-bit hue logic for cognitive flow management. 
Implements -1 (gray), 0 (black), +1 (white) states for trait routing and entropy control.
""",
    "qbithue_reflex_interpreter.py": """# qbithue_reflex_interpreter.py

Analyzes the Qbithue network to detect reflexive connections between nodes.
Used as a basis for building subconscious behavior patterns.
""",
    "qbithue_resonance_engine.py": """# qbithue_resonance_engine.py

Evaluates and adjusts node resonance values within the Qbithue network.
Ensures trait stability and reflective capacity within token relationships.
""",
    "queens_fold_initializer.py": """# queens_fold_initializer.py

Initializes the Queen’s Fold layer, generating a trust signature and 
secure metadata anchor for downstream protocol enforcement.
""",
    "subconscious_router.py": """# subconscious_router.py

Establishes subconscious pathways by analyzing reflex connections.
Lays down implicit behavior routes prior to conscious interpretation.
""",
    "trait_anchor_relinker.py": """# trait_anchor_relinker.py

Relinks trait anchors by evaluating recent trait elevation data.
Ensures continuous alignment of memory structures as traits evolve.
""",
    "trait_elevation_engine.py": """# trait_elevation_engine.py

Scans the reflex arcs to elevate potential traits based on thresholds.
Creates a promoted trait log for further linking and conscious evaluation.
""",
    "trait_inheritance_binder.py": """# trait_inheritance_binder.py

Links elevated traits based on observed path overlaps.
Binds patterns together as inherited behavior across cognitive cycles.

____________________________________________________________________________

## q_node.py

This module defines the `QNode` class, which represents a cognition-aware node
capable of operating across conscious and subconscious logic layers.

QNode integrates a `QLayerToken` to:
- Simulate Q-state shifts (subconscious, static, conscious)
- React to fluorescence tags (e.g., 'memory', 'logic')
- Adjust token behavior via simulated EM field input
- Build neural bridges across logic flows

Each QNode is linkable to other QNodes for reflex pattern formation and trait elevation paths.

## test_q_node.py

This file tests the functionality of `QNode`, including:
- Token initialization
- Fluorescence tagging
- Conscious state shifts
- Electromagnetic field state updates
- Node linking behavior

To run the test:

```bash
PYTHONPATH=. python3 scripts/test_q_node.py

_______----------------output-----------------_______________

Node A:
{'type': 'logic', 'token': {'color': (0, 255, 0), 'fluorescence': ['reflex'], 'q_state': 1, 'field': {'frequency': 19.7, 'amplitude': 0.81}, 'mode': 'propagate'}, 'connected_to': 'memory'}

Node B:
{'type': 'memory', 'token': {'color': (0, 0, 255), 'fluorescence': [], 'q_state': 0, 'field': {'frequency': 0.0, 'amplitude': 0.0}, 'mode': 'propagate'}, 'connected_to': None}

________________________________________________________________________________________

## q_layer_token.py

This script provides a reusable logic engine for handling Q-layer token behavior across AI-Core.

Functions:
- `generate_q_token()` — Create a token with color, tag(s), and mode.
- `route_token()` — Apply simulated EM field routing (frequency + amplitude).
- `adjust_fluorescence()` — Add or clear fluorescence tags.
- `shift_token_q_state()` — Set the Q-state (-1: subconscious, 0: static, +1: conscious).

Used to power memory routing, node logic, trait elevation, and system behavior layers.

## test_q_layer_token_engine.py

Tests the `q_layer_token.py` engine. Validates token creation, state mutation, field propagation, and functional overlays.

Run with:

```bash
PYTHONPATH=. python3 scripts/test_q_layer_token_engine.py

_______________________----------output-----------________________________

[Step 1] Generated Token:
{'color': (128, 0, 255), 'fluorescence': ['init'], 'q_state': 0, 'field': {'frequency': 0.0, 'amplitude': 0.0}, 'mode': 'propagate'}

[Step 2] Added 'logic' Fluorescence:
{'color': (128, 0, 255), 'fluorescence': ['init', 'logic'], 'q_state': 0, 'field': {'frequency': 0.0, 'amplitude': 0.0}, 'mode': 'propagate'}

[Step 3] Shifted Q-State to +1:
{'color': (128, 0, 255), 'fluorescence': ['init', 'logic'], 'q_state': 1, 'field': {'frequency': 0.0, 'amplitude': 0.0}, 'mode': 'propagate'}

[Step 4] Routed Token with EM Field:
{'color': (128, 0, 255), 'fluorescence': ['init', 'logic'], 'q_state': 1, 'field': {'frequency': 22.4, 'amplitude': 0.94}, 'mode': 'propagate'}

________________________________________________________________________________________________________

## em_field_balancer.py

Simulates a dynamic electromagnetic field that regulates cognitive energy in AI-Core systems.

Fields:
- `internal_fluctuation` – chaos/tension from within (e.g., trait conflict)
- `external_resistance` – outside pressure (e.g., complex memory load)
- `field_strength` – cognitive energy pool available for recall and routing

Methods:
- `detect_fluctuations()` – simulates internal disturbance
- `detect_resistance()` – simulates resistance from external demands
- `balance_field()` – uses energy to stabilize the system
- `apply_force()` – applies field effort for targeted action
- `report()` – returns current field state

Intended to power future Q-layer decisions, memory access priority, and cognitive thread balancing.

-------------

## test_em_field_balancer.py

Tests the `ElectromagneticField` class by simulating a full cycle of:

- Internal fluctuation detection
- External resistance simulation
- Field balancing through kinetic energy
- Application of force to maintain stability
- Final report of remaining field strength

Run it with:

```bash
PYTHONPATH=. python3 scripts/test_em_field_balancer.py

__________________-------------output------------________________

[Step 1] Internal Fluctuation: 2.93
[Step 2] External Resistance: 2.20
[Step 3] Applied 7.70 units of kinetic energy to stabilize.
[Step 4] Applied 14.57 units of field force.

[Final State]
field_strength: 977.73
internal_fluctuation: 2.93
external_resistance: 2.20

________________________________________________________________________________

### test_electromagnetic_field.py

This test script simulates a one-time run of the ElectromagneticField system.
It initializes the field, detects random fluctuations and resistance, balances the field, and applies force.
The output includes internal state and final field strength for verification.

scripts/test_electromagnetic_field.py
test with 
PYTHONPATH=. python3 scripts/test_electromagnetic_field.py


_________________-----------------------output-----------------_____________

[Test] Initializing Electromagnetic Field with strength 1000.0

[Test] Detecting internal fluctuation...
[Step 1] Internal Fluctuation: -7.27
[Test] Detecting external resistance...
[Step 2] External Resistance: 0.20
[Test] Balancing field...
[Step 3] Applied -10.61 units of kinetic energy to stabilize.
[Test] Applying force...
[Step 4] Applied 14.45 units of field force.

[Result] Final State:
field_strength: 996.16
internal_fluctuation: -7.27
external_resistance: 0.20

__________________________________________________________________________________________

### test_energy_pool.py

This test script verifies the functionality of `energy_pool.py`, which manages energy flow between a central pool and a rechargeable battery unit. It performs:

- Energy push into the battery (with overflow logic).
- Energy pull prioritizing battery usage before falling back to the main pool.
- Displays final energy state for validation.

Used to simulate energy regulation within AI-Core’s electromagnetic and cognitive subsystems.

scripts/test_energy_pool.py
test with
python3 scripts/test_energy_pool.py

_______________________________________________------------output---------____________

[Test] Initializing EnergyPool with battery capacity = 500

[Test] Pushing 300 energy into battery...
Pushed 300 energy into the battery. Battery storage: 300

[Test] Pulling 200 energy...
Pulled 200 from the battery. Battery storage: 100

[Test] Pulling 400 energy (should deplete battery and use pool)...
Pulled 100 from the battery. Now pulling 300 from the pool.
Pulled 300 energy from the pool. Remaining pool energy: 700

[Test] Pushing 600 energy (should overflow into pool)...
Battery full! Pushed 100 energy into the pool. Pool energy: 800

[Result] Final Energy States:
  Battery Storage: 500
  Pool Energy: 800

  _____________________________________________________________________________________

  ### test_energy_nodes.py

**Purpose**: Tests interaction of `energy_node.py` and `energy_node_2.py` using simultaneous task and energy logic simulation.

**Behavior**:
- Initializes two nodes with different energy levels.
- Runs 3 cycles:
  - Each node performs a task (complexity increases per cycle).
  - Each node flips state (simulates energy exchange).
- Tracks and prints:
  - Remaining energy
  - Energy requests and contributions

**Outcome**:
- Confirms energy logic, state flipping, and task performance work across both implementations.

scripts/test_energy_nodes.py
test with 
python3 scripts/test_energy_nodes.py