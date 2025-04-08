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
