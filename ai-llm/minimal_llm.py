import sys
import os
sys.path.append(os.path.abspath(".."))

import numpy as np
from training.training_pairs import training_pairs

import csv

def load_tokens(csv_path):
    tokens = []
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            # Parse binary values only (Hue, R, G, B)
            hue_bin = row[0]
            r_bin = row[1]
            g_bin = row[2]
            b_bin = row[3]
            # Convert binary strings to floats (0 or 1 bits)
            token_vec = [int(b) for b in hue_bin + r_bin + g_bin + b_bin]
            tokens.append(token_vec)
    return np.array(tokens)


class MinimalLLM:
    def __init__(self, input_size, hidden_size, output_size):
        # Random weights
        self.W1 = np.random.randn(input_size, hidden_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size)
        self.b2 = np.zeros((1, output_size))

    def forward(self, x):
        # Simple feedforward pass
        z1 = x @ self.W1 + self.b1
        a1 = np.tanh(z1)
        z2 = a1 @ self.W2 + self.b2
        return z2


    def train_step(self, x, y, learning_rate=0.01):
        # Forward pass
        z1 = x @ self.W1 + self.b1
        a1 = np.tanh(z1)
        z2 = a1 @ self.W2 + self.b2
        output = z2

        # Backward pass (mean squared error loss)
        d_loss = 2 * (output - y) / y.size
        d_W2 = a1.T @ d_loss
        d_b2 = np.sum(d_loss, axis=0, keepdims=True)

        d_a1 = d_loss @ self.W2.T
        d_z1 = d_a1 * (1 - np.tanh(z1) ** 2)

        d_W1 = x.T @ d_z1
        d_b1 = np.sum(d_z1, axis=0, keepdims=True)

        # Gradient descent update
        self.W1 -= learning_rate * d_W1
        self.b1 -= learning_rate * d_b1
        self.W2 -= learning_rate * d_W2
        self.b2 -= learning_rate * d_b2

        # Return loss
        return np.mean((output - y) ** 2)



def mean_squared_error(predicted, target):
    return np.mean((predicted - target) ** 2)


def main():
    tokens = load_tokens("../tokenizer/full_color_tokens.csv")
    model = MinimalLLM(input_size=tokens[0].shape[0], hidden_size=8, output_size=tokens[0].shape[0])
    print("Training on token pairs:")
    for i, (input_idx, target_idx) in enumerate(training_pairs):
        input_sample = tokens[input_idx].reshape(1, -1)
        target_sample = tokens[target_idx].reshape(1, -1)

        loss = model.train_step(input_sample, target_sample, learning_rate=0.01)
        print(f"Pair {i+1}: Loss = {loss:.6f}")

if __name__ == "__main__":
    main()
