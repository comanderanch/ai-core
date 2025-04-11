import numpy as np
import json
from datetime import datetime

TRAIL_LOG_PATH = "token_trail_log.json"

def log_token_activity(input_index, output_vector):
    """Logs the input index and the resulting output vector into a memory trail file."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "input_index": input_index,
        "output_summary": {
            "mean": float(np.mean(output_vector)),
            "max": float(np.max(output_vector)),
            "min": float(np.min(output_vector))
        }
    }

    try:
        with open(TRAIL_LOG_PATH, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(log_entry)

    with open(TRAIL_LOG_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Logged token activity for index {input_index}")
