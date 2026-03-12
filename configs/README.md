# configs
Description for the configs directory.

# Configs

This directory contains configuration files and presets for the AI system.

## Purpose
- Define startup parameters, environment variables, and system-wide options.
- Load customizable values for different AI modes, memory behaviors, and token handling.
- Support quick swapping of config sets for testing or deployment.

## Suggested Files
- `default.json` – Baseline settings used on initial boot.
- `dev.json` – Development-specific overrides.
- `modes/` – Optional subfolder for state-based config profiles (e.g., passive, aggressive, reflective).

## Notes
Configs are meant to be human-readable and modular.  
Avoid hardcoding values in the engine; route them through these files instead.
