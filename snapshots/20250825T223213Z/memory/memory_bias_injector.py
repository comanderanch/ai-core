# memory/memory_bias_injector.py

import json
import os

MEMORY_BIAS_LOG = os.path.join(os.path.dirname(__file__), "memory_bias_log.json")

def inject_bias(label, bias):
    entry = {"label": label, "bias": bias}

    # Load old log if exists
    if os.path.exists(MEMORY_BIAS_LOG):
        with open(MEMORY_BIAS_LOG, "r") as file:
            log = json.load(file)
    else:
        log = []

    log.append(entry)

    with open(MEMORY_BIAS_LOG, "w") as file:
        json.dump(log, file, indent=2)

    print(f"[INJECT] Bias for '{label}' recorded: {bias}")
