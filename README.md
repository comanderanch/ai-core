# AI-Core: Token-Based Modular Intelligence System

**AI-Core** is a custom full-stack framework for building tokenized intelligence systems from the ground up — bypassing transformer dependency and black-box embeddings.

This isn’t a typical LLM project.

AI-Core operates through:
- Color → Binary tokenization
- Slot/Matrix address mapping
- Q-layer state logic anchoring
- Frequency-aligned memory binding

Every component is auditable, modular, and designed to simulate self-evolving structure over time.

> ⚠️ Some systems are intentionally not shown in this public repo.  
> Due to token scale, memory slot expansion, and live testing across multiple dev machines, several builds are running in parallel in my private network.

What’s visible here is just the **core** — the base spine.  
The living system continues to evolve.

---



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

_______________________________________________________________


---

## 📦 Phase 33 – CSV-Based Training Integration

This phase replaces static `training_pairs.py` with a dynamic, scalable loader system using:

- **File:** `training_set.csv`
- **Loader:** `training_loader.py`
- **Bridge Module:** `training_from_csv.py`

### CSV Schema:
| input_token | target_token | label  | weight |
|-------------|--------------|--------|--------|
| 10          | 25           | Hot    | 1.0    |
| 15          | 30           | Cold   | 1.0    |

### Usage:
Import the `training_data` list from `training_from_csv.py` in any training script:

```python
from training.training_from_csv import training_data

_______________________________________________________

---

## 🧠 Phase 33.2 – Training Logic Rewrite (CSV Pipeline)

- **Script:** `train_model_from_csv.py`
- **Input:** `training_set.csv` (via `training_from_csv.py`)
- **Behavior:** Simulates LLM training loop with labeled token transitions

### Example Output:

_______________________________________________________

[TRAINING] 10 ➡ 25 | Label: 'Hot' | Weight: 1.0



> Malformed or incomplete rows in the CSV are skipped with a warning, allowing robust handling during development.

This script now serves as the foundation for live training loop integration with the token reflex pipeline in future phases.

_______________________________________________________

- `training_set.csv` – Structured CSV format including input token, target token, label, and weight. Enables associative learning.

________________________________________________________

✅ training_loader.py
Already in use and tested via load_training_data() ✔️

________________________________________________

- `training_from_csv.py` – Parses structured training data from CSV into memory for model training access.
🆕 train_model_from_csv.py
Also to training/README.md:

_______________________________________________

- `train_model_from_csv.py` – Loads CSV data and simulates minimal token-based learning with label association output.

_________________________________________________


New scripts:

training_loader.py — Loads structured token training data from CSV.

training_from_csv.py — Imports and provides access to loaded training pairs for training scripts.

train_model_from_csv.py — Executes basic training on token pairs with weights and labels.

training_set.csv — CSV file storing token pair input/target, label, and weight for structured training.

Also mark:

training_pairs.py — ✅ Deleted (mention replaced by CSV flow)

_______________________________________________________
