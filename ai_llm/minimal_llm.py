import numpy as np

# MinimalLLM: A simple feedforward neural network for token prediction
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

                # Forward pass
                z1 = x @ self.W1 + self.b1
                a1 = np.tanh(z1)
                z2 = a1 @ self.W2 + self.b2
                output = z2

                # Backpropagation (MSE loss)
                d_loss = 2 * (output - y) / y.size
                d_W2 = a1.T @ d_loss
                d_b2 = np.sum(d_loss, axis=0, keepdims=True)

                d_a1 = d_loss @ self.W2.T
                d_z1 = d_a1 * (1 - np.tanh(z1) ** 2)
                d_W1 = x.T @ d_z1
                d_b1 = np.sum(d_z1, axis=0, keepdims=True)

                # Gradient descent update
                self.W1 -= learning_rate * d_W1 * w
                self.b1 -= learning_rate * d_b1 * w
                self.W2 -= learning_rate * d_W2 * w
                self.b2 -= learning_rate * d_b2 * w

                total_loss += np.mean((output - y) ** 2) * w

            loss_history.append(total_loss / len(x_batch))

        return loss_history


def save_model(model, path="model_weights.npz"):
    np.savez(path, W1=model.W1, b1=model.b1, W2=model.W2, b2=model.b2)


def load_model(model, path="model_weights.npz"):
    data = np.load(path)
    model.W1 = data["W1"]
    model.b1 = data["b1"]
    model.W2 = data["W2"]
    model.b2 = data["b2"]


def mean_squared_error(predicted, target):
    return np.mean((predicted - target) ** 2)


def cosine_similarity(a, b):
    a = a.flatten()
    b = b.flatten()
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)

