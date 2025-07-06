import json
from pathlib import Path
from datetime import datetime
import numpy as np
import sys
sys.path.append("ai-llm")

from minimal_llm import MinimalLLM


# Load config
with open("configs/training_config.json", "r") as f:
    config = json.load(f)

input_path = Path(config["input_file"])
output_path = Path(config["output_log"])

# Verify input file exists
if not input_path.exists():
    raise FileNotFoundError(f"Input file not found: {input_path}")

# Create output log if it doesn't exist
if not output_path.exists():
    log_data = {
        "training_status": "initialized",
        "start_time": datetime.utcnow().isoformat(),
        "end_time": None,
        "epochs_completed": 0,
        "errors": [],
        "output_summary": {}
    }
    with open(output_path, "w") as f:
        json.dump(log_data, f, indent=2)
    print(f"[✓] Log initialized: {output_path}")
else:
    print(f"[✓] Log file already exists: {output_path}")

# === Model Bootstrap Interface ===
input_size = 3
hidden_size = 5
output_size = 1

try:
    model = MinimalLLM(input_size, hidden_size, output_size)
    print("[✓] Model initialized.")

    # Update log with model status
    with open(output_path, "r") as f:
        log_data = json.load(f)

    log_data["training_status"] = "model_initialized"

    with open(output_path, "w") as f:
        json.dump(log_data, f, indent=2)

except Exception as e:
    print(f"[✗] Model initialization failed: {e}")

    with open(output_path, "r") as f:
        log_data = json.load(f)

    log_data["errors"].append(str(e))
    log_data["training_status"] = "error"

    with open(output_path, "w") as f:
        json.dump(log_data, f, indent=2)

import csv

# === Load and prepare CSV data ===
def load_csv_data(path):
    with open(path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        data = []
        for row in reader:
            if len(row) < 4:
                continue  # Skip malformed rows
            try:
                # Extract and convert numeric fields only
                input_token = float(row[0])
                target_token = float(row[1])
                weight = float(row[3])
                data.append([input_token, target_token, weight])
            except ValueError:
                continue  # Skip non-numeric or corrupt rows

    data = np.array(data)
    x_data = data[:, :2]  # input_token, target_token
    y_data = data[:, 2:]  # weight
    return x_data, y_data

# === Run Data Load ===
try:
    x_data, y_data = load_csv_data(input_path)
    print(f"[✓] Loaded {len(x_data)} training samples.")
    
    # Log sample load
    with open(output_path, "r") as f:
        log_data = json.load(f)

    log_data["training_status"] = "data_loaded"
    log_data["sample_count"] = len(x_data)

    with open(output_path, "w") as f:
        json.dump(log_data, f, indent=2)

except Exception as e:
    print(f"[✗] Failed to load training data: {e}")

    with open(output_path, "r") as f:
        log_data = json.load(f)

    log_data["errors"].append(f"Data load error: {str(e)}")
    log_data["training_status"] = "error"

    with open(output_path, "w") as f:
        json.dump(log_data, f, indent=2)
