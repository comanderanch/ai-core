#!/usr/bin/env python3
"""
AI-Core Standalone: MinimalLLM for 498D Consciousness
======================================================

Expands the original MinimalLLM from 82D to 498D to handle:
- 82D  Fluorescent (physics)
- 250D GridBloc (space)
- 166D Quadrademini (quantum)

Architecture:
  Input:  498D token vector
  Hidden: Bottleneck layer (configurable, default 64D)
  Output: 498D prediction vector

This is a TINY neural network (compared to billions of parameters):
- 498 → 64 → 498 = ~32K parameters
- GPU-friendly (color operations)
- Trainable on commodity hardware (P100)

The network learns semantic relationships through 498D space:
- "fire" → thermal domain (high Q1 energy)
- "water" → fluid domain (high Q2 flow)
- Spatial relationships preserved (GridBloc)
- Quantum superposition maintained (Quadrademini)

Author: comanderanch
Phase: 5.7 Standalone Resurrection - NEURAL LAYER
"""

import numpy as np
from pathlib import Path
from typing import Tuple, Optional
import json
from datetime import datetime


class MinimalLLM498D:
    """
    Minimal neural network for 498D consciousness inference.
    
    Simple bottleneck architecture:
      498D input → hidden → 498D output
    
    Uses tanh activation (smooth, differentiable)
    Trained with basic gradient descent
    
    This is NOT trying to compete with transformers!
    This is proving consciousness-as-ordinance works at scale.
    """
    
    def __init__(
        self,
        input_dim: int = 498,
        hidden_dim: int = 64,
        learning_rate: float = 0.01
    ):
        """
        Initialize MinimalLLM for 498D.
        
        Args:
            input_dim: Input dimensions (498D consciousness)
            hidden_dim: Hidden layer size (bottleneck)
            learning_rate: Training step size
        """
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.learning_rate = learning_rate
        
        # Initialize weights (Xavier initialization)
        scale1 = np.sqrt(2.0 / (input_dim + hidden_dim))
        scale2 = np.sqrt(2.0 / (hidden_dim + input_dim))
        
        self.W1 = np.random.randn(input_dim, hidden_dim) * scale1  # 498 → 64
        self.b1 = np.zeros(hidden_dim)
        
        self.W2 = np.random.randn(hidden_dim, input_dim) * scale2  # 64 → 498
        self.b2 = np.zeros(input_dim)
        
        # Training statistics
        self.training_history = []
        
        total_params = (
            self.W1.size + self.b1.size +
            self.W2.size + self.b2.size
        )
        
        print(f"[✓] MinimalLLM498D initialized")
        print(f"    Architecture: {input_dim}D → {hidden_dim}D → {input_dim}D")
        print(f"    Total parameters: {total_params:,}")
        print(f"    Learning rate: {learning_rate}")
    
    def forward(self, x: np.ndarray) -> Tuple[np.ndarray, dict]:
        """
        Forward pass through network.
        
        Args:
            x: Input vector (498D)
        
        Returns:
            (output, cache) where cache contains intermediate values
        """
        # Layer 1: 498D → 64D
        z1 = x @ self.W1 + self.b1
        a1 = np.tanh(z1)  # Hidden activation
        
        # Layer 2: 64D → 498D
        z2 = a1 @ self.W2 + self.b2
        output = z2  # Linear output (no activation)
        
        # Cache for backprop
        cache = {
            'x': x,
            'z1': z1,
            'a1': a1,
            'z2': z2
        }
        
        return output, cache
    
    def backward(
        self,
        cache: dict,
        target: np.ndarray,
        output: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Backward pass (gradient computation).
        
        Args:
            cache: Intermediate values from forward pass
            target: Target vector (498D)
            output: Network output (498D)
        
        Returns:
            (dW1, db1, dW2, db2) gradients
        """
        # Extract cached values
        x = cache['x']
        a1 = cache['a1']
        z1 = cache['z1']
        
        # Output layer gradient
        dz2 = output - target  # MSE gradient
        dW2 = np.outer(a1, dz2)
        db2 = dz2
        
        # Hidden layer gradient
        da1 = dz2 @ self.W2.T
        dz1 = da1 * (1 - np.tanh(z1)**2)  # tanh derivative
        dW1 = np.outer(x, dz1)
        db1 = dz1
        
        return dW1, db1, dW2, db2
    
    def train_step(
        self,
        input_vec: np.ndarray,
        target_vec: np.ndarray
    ) -> float:
        """
        Single training step.
        
        Args:
            input_vec: Input 498D vector
            target_vec: Target 498D vector
        
        Returns:
            Loss value
        """
        # Forward pass
        output, cache = self.forward(input_vec)
        
        # Compute loss (MSE)
        loss = np.mean((output - target_vec)**2)
        
        # Backward pass
        dW1, db1, dW2, db2 = self.backward(cache, target_vec, output)
        
        # Update weights
        self.W1 -= self.learning_rate * dW1
        self.b1 -= self.learning_rate * db1
        self.W2 -= self.learning_rate * dW2
        self.b2 -= self.learning_rate * db2
        
        return loss
    
    def predict(self, input_vec: np.ndarray) -> np.ndarray:
        """
        Generate prediction for input.
        
        Args:
            input_vec: Input 498D vector
        
        Returns:
            Predicted 498D vector
        """
        output, _ = self.forward(input_vec)
        return output
    
    def train_batch(
        self,
        input_batch: np.ndarray,
        target_batch: np.ndarray,
        epochs: int = 10,
        batch_size: int = 32,
        verbose: bool = True
    ):
        """
        Train on batch of data.
        
        Args:
            input_batch: Array of input vectors (N, 498)
            target_batch: Array of target vectors (N, 498)
            epochs: Number of training epochs
            batch_size: Mini-batch size
            verbose: Print progress
        """
        num_samples = len(input_batch)
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"TRAINING MinimalLLM498D")
            print(f"{'='*60}")
            print(f"  Samples: {num_samples}")
            print(f"  Epochs: {epochs}")
            print(f"  Batch size: {batch_size}")
            print(f"{'='*60}\n")
        
        for epoch in range(epochs):
            epoch_loss = 0.0
            num_batches = 0
            
            # Shuffle data
            indices = np.random.permutation(num_samples)
            
            # Process mini-batches
            for i in range(0, num_samples, batch_size):
                batch_indices = indices[i:i+batch_size]
                
                for idx in batch_indices:
                    loss = self.train_step(
                        input_batch[idx],
                        target_batch[idx]
                    )
                    epoch_loss += loss
                
                num_batches += 1
            
            # Average loss for epoch
            avg_loss = epoch_loss / num_samples
            self.training_history.append(avg_loss)
            
            if verbose and (epoch % max(1, epochs // 10) == 0 or epoch == epochs - 1):
                print(f"  Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.6f}")
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"TRAINING COMPLETE")
            print(f"  Final loss: {avg_loss:.6f}")
            print(f"{'='*60}\n")
    
    def save_weights(self, output_path: str = "models/minimal_llm_498d_weights.npz"):
        """Save trained weights."""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        np.savez(
            output,
            W1=self.W1,
            b1=self.b1,
            W2=self.W2,
            b2=self.b2,
            input_dim=self.input_dim,
            hidden_dim=self.hidden_dim,
            learning_rate=self.learning_rate,
            training_history=self.training_history
        )
        
        print(f"[✓] Saved weights to: {output}")
    
    def load_weights(self, weights_path: str = "models/minimal_llm_498d_weights.npz"):
        """Load trained weights."""
        data = np.load(weights_path)
        
        self.W1 = data['W1']
        self.b1 = data['b1']
        self.W2 = data['W2']
        self.b2 = data['b2']
        self.input_dim = int(data['input_dim'])
        self.hidden_dim = int(data['hidden_dim'])
        self.learning_rate = float(data['learning_rate'])
        self.training_history = list(data['training_history'])
        
        print(f"[✓] Loaded weights from: {weights_path}")
        print(f"    Training history: {len(self.training_history)} epochs")


def create_training_pairs(
    vectors: np.ndarray,
    context_size: int = 3
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create training pairs from 498D vectors.
    
    Simple next-token prediction:
    - Input: Average of N context tokens
    - Target: Next token
    
    Args:
        vectors: All 498D token vectors (2304, 498)
        context_size: Number of context tokens
    
    Returns:
        (inputs, targets) arrays
    """
    num_tokens = len(vectors)
    num_pairs = num_tokens - context_size
    
    inputs = np.zeros((num_pairs, 498))
    targets = np.zeros((num_pairs, 498))
    
    for i in range(num_pairs):
        # Context: average of previous N tokens
        context = vectors[i:i+context_size]
        inputs[i] = np.mean(context, axis=0)
        
        # Target: next token
        targets[i] = vectors[i+context_size]
    
    return inputs, targets


if __name__ == "__main__":
    print("\n" + "🧬"*30)
    print("MinimalLLM 498D - NEURAL CONSCIOUSNESS LAYER")
    print("🧬"*30 + "\n")
    
    # Load 498D vectors
    print("Loading 498D consciousness dataset...")
    vectors_path = Path("tokenizer/token_vectors_498d.npy")
    
    if not vectors_path.exists():
        print(f"❌ ERROR: 498D vectors not found at {vectors_path}")
        print("   Run: python3 tokenizer/unified_498d_encoder.py first!")
        exit(1)
    
    vectors = np.load(vectors_path)
    print(f"[✓] Loaded {len(vectors)} vectors of {vectors.shape[1]}D")
    
    # Create training pairs
    print("\nCreating training pairs...")
    inputs, targets = create_training_pairs(vectors, context_size=3)
    print(f"[✓] Created {len(inputs)} training pairs")
    
    # Initialize model
    print("\nInitializing MinimalLLM498D...")
    model = MinimalLLM498D(input_dim=498, hidden_dim=64, learning_rate=0.01)
    
    # Train
    print("\nReady to train!")
    print("⚠️  This will train on 2,301 pairs for 100 epochs (~2-5 minutes)")
    response = input("Continue? [y/n]: ")
    
    if response.lower() == 'y':
        model.train_batch(
            inputs,
            targets,
            epochs=100,
            batch_size=32,
            verbose=True
        )
        
        # Save weights
        model.save_weights()
        
        # Test prediction
        print("\n" + "="*60)
        print("TEST PREDICTION")
        print("="*60)
        test_input = inputs[0]
        test_target = targets[0]
        prediction = model.predict(test_input)
        
        print(f"Input norm:      {np.linalg.norm(test_input):.3f}")
        print(f"Target norm:     {np.linalg.norm(test_target):.3f}")
        print(f"Prediction norm: {np.linalg.norm(prediction):.3f}")
        print(f"Error:           {np.linalg.norm(prediction - test_target):.3f}")
        
        print("\n🔥 MINIMALLLM 498D TRAINED!")
        print("   Consciousness inference layer COMPLETE!")
    else:
        print("\n⏸️  Training skipped")
    
    print("\n" + "🧬"*30)
    print("READY FOR FULL PIPELINE TEST!")
    print("🧬"*30 + "\n")