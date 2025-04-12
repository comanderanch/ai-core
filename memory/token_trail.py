import os
import json
import numpy as np
from datetime import datetime

# Always resolve path relative to this script’s location
TRAIL_LOG_PATH = os.path.join(os.path.dirname(__file__), "token_trail_log.json")

def log_token_activity(index, prediction, path=TRAIL_LOG_PATH):
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "input_index": index,
        "output_summary": {
            "mean": float(np.mean(prediction)),
            "max": float(np.max(prediction)),
            "min": float(np.min(prediction)),
        }
    }

    if os.path.exists(path):
        with open(path, "r") as f:
            log = json.load(f)
    else:
        log = []

    log.append(summary)

    with open(path, "w") as f:
        json.dump(log, f, indent=2)

    print(f"Logged token activity for index {index}")
