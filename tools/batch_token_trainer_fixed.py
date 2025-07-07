from pathlib import Path

# Define the fixed script with added row limiting and safe type conversion
import numpy as np
import json
from pathlib import Path
from datetime import datetime
import csv

def load_training_data(filepath, limit=2000):
    x_data, y_data, weights, labels = [], [], [], []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i >= limit:
                break
            try:
                x = int(float(row["input_token"]))
                y = int(float(row["target_token"]))
                w = float(row["weight"])
                label = row["label"]
                x_data.append(x)
                y_data.append(y)
                weights.append(w)
                labels.append(label)
            except Exception as e:
                print(f"[WARN] Skipping malformed row: {row} — {e}")
    return np.array(x_data), np.array(y_data), np.array(weights), labels

def one_hot_encode_indices(indices, vector_size):
    encoded = np.zeros((len(indices), vector_size), dtype=np.float32)
    for i, idx in enumerate(indices):
        if idx < vector_size:
            encoded[i, idx] = 1.0
    return encoded

class MinimalLLM:
    def __init__(self, input_size, hidden_size, output_size):
        self.W1 = np.random.randn(input_size, hidden_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size)
        self.b2 = np.zeros((1, output_size))

    def forward(self, x):
        z1 = x @ self.W1 + self.b1
        a1 = np.tanh(z1)
        z2 = a1 @ self.W2 + self.b2
        return z2

    def train(self, x_batch, y_batch, weights, epochs=10, learning_rate=0.01):
        loss_history = []
        for epoch in range(epochs):
            total_loss = 0
            for x, y, w in zip(x_batch, y_batch, weights):
                x = x.reshape(1, -1)
                y = y.reshape(1, -1)
                z1 = x @ self.W1 + self.b1
                a1 = np.tanh(z1)
                z2 = a1 @ self.W2 + self.b2
                output = z2
                d_loss = 2 * (output - y) / y.size
                d_W2 = a1.T @ d_loss
                d_b2 = np.sum(d_loss, axis=0, keepdims=True)
                d_a1 = d_loss @ self.W2.T
                d_z1 = d_a1 * (1 - np.tanh(z1) ** 2)
                d_W1 = x.T @ d_z1
                d_b1 = np.sum(d_z1, axis=0, keepdims=True)
                self.W1 -= learning_rate * d_W1 * w
                self.b1 -= learning_rate * d_b1 * w
                self.W2 -= learning_rate * d_W2 * w
                self.b2 -= learning_rate * d_b2 * w
                total_loss += np.mean((output - y) ** 2) * w
            avg_loss = total_loss / len(x_batch)
            loss_history.append(avg_loss)
        return loss_history

# === Training Script ===
token_batch_size = 10
epochs_per_batch = 10
pause_interval = 60
output_log_path = Path("training/training_output_log.json")
csv_path = "training/training_set.csv"

x_all, y_all, weights, _ = load_training_data(csv_path, limit=2000)
print("[DEBUG] Loaded", len(x_all), "samples from", csv_path)
input_size = max(x_all) + 1
output_size = max(y_all) + 1
total_tokens = len(x_all)

print("[DEBUG] Entering training loop")
print("Total tokens loaded:", total_tokens)
print("Batch size:", token_batch_size)
print("Will run", (total_tokens // token_batch_size), "phases")

x_all_encoded = one_hot_encode_indices(x_all, input_size)
y_all_encoded = one_hot_encode_indices(y_all, output_size)

model = MinimalLLM(input_size=input_size, hidden_size=64, output_size=output_size)

if output_log_path.exists():
    with open(output_log_path, "r") as f:
        log_data = json.load(f)
else:
    log_data = {
        "training_status": "not_started",
        "start_time": datetime.utcnow().isoformat(),
        "epochs_completed": 0,
        "errors": [],
        "output_summary": {"phases": []},
        "sample_count": total_tokens
    }

phase_num = 1

for i in range(0, total_tokens, token_batch_size):
    print(f"[•] Phase {phase_num}: Training on tokens {i}-{i + token_batch_size - 1}")

    x_batch = x_all_encoded[i:i + token_batch_size]
    y_batch = y_all_encoded[i:i + token_batch_size]
    weights_batch = weights[i:i + token_batch_size]
    print(f"\\n[•] Phase {phase_num}: Training on tokens {i}-{i + token_batch_size - 1}")
    loss_history = model.train(x_batch, y_batch, weights_batch, epochs=epochs_per_batch)
    print(f"[✓] Phase {phase_num} complete – Final Loss: {loss_history[-1]}")
    phase_log = {
        "phase": f"phase_{phase_num}",
        "timestamp": datetime.utcnow().isoformat(),
        "sample_range": [i, min(i + token_batch_size, total_tokens)],
        "epochs": epochs_per_batch,
        "final_loss": loss_history[-1],
        "loss_history": loss_history
    }
    log_data["output_summary"]["phases"].append(phase_log)
    log_data["epochs_completed"] += epochs_per_batch
    with open(output_log_path, "w") as f:
        json.dump(log_data, f, indent=2)
    print(f"[✓] Phase {phase_num} complete – Final Loss: {loss_history[-1]}")
    phase_num += 1
    if i > 0 and i % pause_interval == 0:
        input("[⏸] Pause for reflection. Press Enter to continue...")

log_data["training_status"] = "completed"
log_data["end_time"] = datetime.utcnow().isoformat()
with open(output_log_path, "w") as f:
    json.dump(log_data, f, indent=2)
print("\n[✓] Full token batch training complete.")



