# tokenizer
Description for the tokenizer directory.

# Tokenizer

This module handles the conversion of raw input (text, audio, or signals) into structured tokens.

## Purpose
- Translate external data into the AI's internal language.
- Enable color-based token representation for increased token resolution.
- Support reverse-tokenization for AI-generated output.

## Modes
- `color_mode` – Primary system using color frequency, hue, and intensity as tokens.
- `text_mode` – Fallback for traditional word/byte tokenization.
- `hybrid_mode` – Optional blend of color and text token layers.

## Components
- `tokenizer.py` / `tokenizer.cpp` – Main logic for encoding/decoding.
- `mappings/` – Data files for color-word associations and spectrum definitions.
- `utils/` – Helpers for token collision checks, token stats, and normalization.

## Notes
This is a critical layer. The quality and structure of tokenization directly influence the AI’s reasoning ability.  
Color token uniqueness is vital — collisions are logged and flagged automatically.

#color_hue_tokenizer.cpp
This C++ program generates a custom token set using hue-based color values instead of standard text tokens.
Each token is structured with binary and RGB values along with a hue-based frequency step.
Output is saved to a CSV file named full_color_tokens.csv.

#Usage

g++ color_hue_tokenizer.cpp -o tokenizer

./tokenizer

#Output

full_color_tokens.csv

Contains the complete set of color tokens for use in training custom LLMs with an alternative token system.

#Purpose

This tokenizer is part of a broader experimental framework to explore tokenizing language via color and frequency,
allowing for a potentially more compact and expressive token set that reduces overhead and expands token space.

______________________________________________________________________________________________________________________

# tokenizer/

Contains token processing logic for AI-Core, including color-based encoding and Q-layer behavior.

## q_layer_token.py

Defines the `QLayerToken` class for advanced cognitive token structures.

Each token includes:
- **base_color**: RGB identity
- **fluorescence_tag**: Function overlay (e.g., logic, memory)
- **q_state**: Qbithue access level (-1: subconscious, 0: static, +1: conscious)
- **field_state**: Dict for frequency and amplitude (EM routing)
- **mode**: Operational mode ('propagate', 'collapse', 'echo')

This enables multi-function, field-driven, superposition-based token logic within the AI-Core system.

## Testing  (python3 tokenizer/test_q_layer_token.py)

The `test_q_layer_token.py` file is included to verify the behavior of the `QLayerToken` class.

It performs:
- Token creation with base color
- Field state assignment
- Fluorescence tagging
- Q-state shifting
- Output verification via `.describe()`

Run it with:

```bash
python3 tokenizer/test_q_layer_token.py

-----------------output------------------------------------------------


Token Description:
{'color': (255, 0, 0), 'fluorescence': ['logic', 'memory'], 'q_state': 1, 'field': {'frequency': 13.5, 'amplitude': 0.72}, 'mode': 'propagate'}


_____________________________________________________________________________________________________________________