# ai-core

This project is the starting point for AI-Core.

## Purpose

- Set up a clean, minimal project structure.
- Initialize Git version control.
- Push to the remote GitHub repository.
- Begin with empty folders and placeholder `README.md` files.

No code or functionality has been added yet. This is the foundational setup only.

# AI-Core: Custom Token-Based AI Framework

Welcome to the AI-Core project -  a full-stack custom AI architecture focused on tokenization through RGB, hue, frequency, and influence vectors.

---

## 🔧 System Status

The following subsystems have been added and actively developed:

- `tokenizer/`  
  ➤ Handles RGB + Hue + Frequency → Binary token generation  
  ➤ Includes `color_hue_tokenizer.cpp`, `full_color_tokens.csv`

- `ai-llm/`  
  ➤ Hosts the Minimal LLM neural engine  
  ➤ Now supports 82D input tokens with local influence mapping  
  ➤ Contains training loops, cosine scoring, PCA visualizations, and inference tools

- `training/`  
  ➤ Stores token training pair definitions  
  ➤ Will evolve into intent/semantic pair training

---

## 🧠 Summary

> This project is building an experimental AI from the ground up —  
> using color-based binary tokenization instead of text-token embeddings.

Every phase is tracked via Git commits.  
For module-specific updates and changelogs, see the `README.md` inside each folder.

More info coming soon at:  
🌐 [https://ai-core.hack-shak.com](https://ai-core.hack-shak.com)

---


## Recent Updates

- Token memory trail logging now active (Phase 5.7)
- Anchor influence now blended during LLM training (Phase 5.6)
- See respective folders (`ai-llm/`, `tokenizer/`) for more.

---

---

## 🧠 Journal Update – Phase 32 Reflection

**Date:** 6-23-2025  
**Checkpoint:** Partial Phase 32 freeze

This section logs the most recent growth in the AI-Core project without erasing any of its roots.

### Progress Summary
- Token memory threading now live
- Added `legacy_thread_binder.py` and `ai_affirmation_bridge.py`
- Initiated long-memory map structure in `memory/thread_binds/` and `memory/sensory/`
- Preparing for deep token training (`token_map.py`, `token_heatmap.py`)

### Upcoming Goals
- Begin token training loop
- Integrate subconscious simulation loop (IRN/SoulSync)
- Establish memory slot weighting using hue polarity math

This isn't just an update — it's a fingerprint of the day the vision clarified.  
The README evolves, but never forgets.


