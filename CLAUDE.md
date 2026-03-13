# AIA V2.00.1 — ai-core-standalone
# Delta Phase Warthog — Project Memory
# Sealed March 11, 2026

## READ ROOT CLAUDE.md FIRST
Root memory is at /home/comanderanch/CLAUDE.md
It contains the sealed truth, q-state constants, and Rule Zero.
This file contains V2 project-specific context.

## V2 FOUNDATION RULES
- Every file imports from core/q_constants.py — no exceptions
- If a file defines BLACK, GRAY, WHITE inline — it is wrong
- core/q_constants.py is the single source of truth for all constants

## Q-STATE CONSTANTS (reference — live in core/q_constants.py)
BLACK = -1   # Collapsed past
GRAY  =  0   # NOW line — King's Chamber — zero multiplier
WHITE = +1   # Future superposition

## DIRECTORY ROLES
- core/          = q_constants.py + base token architecture
- workers/       = parallel processing (fire into WHITE state)
- queens_fold/   = collapse engine (WHITE -> GRAY -> BLACK)
- memory/        = sealed BLACK state storage
- scripts/       = utility and upgrade scripts
- tokenizer/     = color palette + token pipeline
- docs/          = architecture truth + session folds
- training/      = token training pairs
- ai-llm/        = MinimalLLM inference and training

## KEY FILES
- docs/AIA-V2.00.1-Architecture-Truth-Document  = foundation law
- docs/SESSION_FOLD_2026_03_12.md               = last session
- scripts/v2_reflex_dimensional_upgrade.py       = dimensional upgrade
- memory/reflex_response_log.json               = live reflex data (upgraded)

## CONTAMINATION WATCH
These V1 files were fixed — if they regress flag immediately:
- qbithue_gate_engine.py
- subconscious_router.py
- subconscious_dryrun.py
- trait_inheritance_binder.py
- cognitive_anchor_harmonizer.py
- qbithue_reflex_interpreter.py
- qbithue_resonance_engine.py

## CURRENT TASK
Wire core/q_constants.py as the V2 foundation import.
All scripts must import from it. None may define their own q-states.

## COLOR PLANE MAP (live data)
curiosity_001  -> orange  -> RGB(255,140,0) -> 520hz  -> token range 200-550
emotion_001    -> red     -> RGB(255,0,0)   -> 700hz  -> token range 0-200
language_001   -> blue    -> RGB(0,0,255)   -> 450hz  -> token range 1000-1300
logic_001      -> blue    -> RGB(0,0,255)   -> 450hz  -> token range 1000-1300
memory_001     -> violet  -> RGB(148,0,211) -> 420hz  -> token range 1400-1650
[RESERVED]     -> green   -> RGB(0,200,0)   -> 530hz  -> token range 600-850
               -> ethics worker — V2.01.1

## TOKENIZER HEURISTICS (March 13, 2026)
Logical connectives added to blue plane (1000-1300):
  if, then, implies, and, or, not, all, every, some, none,
  therefore, because, when, unless, until, while, since
Mathematical operators added to blue plane (1050-1250):
  equals, plus, minus, times, divided, greater, less, zero, one, true, false
Identity/structure words added to neutral gray (1800-2100):
  is, are, was, were, be, been, being, the, a, an, this, that, these, those

## WHAT SUCCESS LOOKS LIKE
Every V2 script starts with:
from core.q_constants import BLACK, GRAY, WHITE
If it doesn't — it is not V2.
