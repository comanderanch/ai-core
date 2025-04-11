import numpy as np

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

def main():
    tokens = load_tokens("../tokenizer/full_color_tokens.csv")
    input_sample = tokens[10].reshape(1, -1)
    model = MinimalLLM(input_size=input_sample.shape[1], hidden_size=8, output_size=4)
    print("Input sample:", input_sample)
    output = model.forward(input_sample)
    print("Output:", output)

if __name__ == "__main__":
    main()
