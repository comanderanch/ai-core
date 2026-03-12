#!/usr/bin/env python3
"""
AI-Core Standalone: GPU Training with Diversity Penalty
========================================================

Modified trainer that penalizes repetitive predictions,
forcing the model to learn diverse semantic associations.

Author: comanderanch
Phase: 5.7 Standalone Resurrection - Diversity Fix
"""

import sys
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict
import json
from collections import Counter


class DiverseMinimalLLMTrainer:
    """
    MinimalLLM trainer with diversity penalty.
    
    Modification: Adds penalty for predicting same token repeatedly.
    Forces model to learn diverse semantic associations.
    """
    
    def __init__(
        self,
        pairs_file: str = "training/massive_semantic_pairs.txt",
        weights_output: str = "memory/model_weights.npz",
        vectors_output: str = "tokenizer/token_influence_vectors.npy",
        learning_rate: float = 0.001,
        epochs: int = 200,
        batch_size: int = 32,
        diversity_weight: float = 0.3  # NEW: Diversity penalty strength
    ):
        """Initialize trainer with diversity penalty."""
        self.pairs_file = Path(pairs_file)
        self.weights_output = Path(weights_output)
        self.vectors_output = Path(vectors_output)
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        self.diversity_weight = diversity_weight
        
        # Model architecture
        self.input_dim = 82
        self.hidden_dim = 32  # Already bigger
        self.output_dim = 82
        
        # Initialize weights
        self.W1 = np.random.randn(self.input_dim, self.hidden_dim) * 0.1
        self.W2 = np.random.randn(self.hidden_dim, self.output_dim) * 0.1
        
        # Token vectors
        self.token_vectors = np.zeros((2304, 82))
        
        # Training data
        self.training_pairs = []
        self.token_usage = {}
        
        # NEW: Track predictions for diversity
        self.recent_predictions = []
        self.prediction_window = 100  # Track last 100 predictions
        
        # Statistics
        self.losses = []
        self.diversity_scores = []
        self.checkpoint_interval = 1000
        
        print(f"[✓] Diverse MinimalLLM Trainer initialized")
        print(f"    Architecture: {self.input_dim} → {self.hidden_dim} → {self.output_dim}")
        print(f"    Diversity penalty: {self.diversity_weight}")
    
    def load_training_pairs(self):
        """Load semantic pairs."""
        print(f"\n[*] Loading training pairs from: {self.pairs_file}")
        
        with open(self.pairs_file, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                
                parts = line.strip().split()
                if len(parts) != 4:
                    continue
                
                word1, word2, tokens1_str, tokens2_str = parts
                tokens1 = [int(t) for t in tokens1_str.split(',')]
                tokens2 = [int(t) for t in tokens2_str.split(',')]
                
                self.training_pairs.append({
                    'word1': word1,
                    'word2': word2,
                    'tokens1': tokens1,
                    'tokens2': tokens2
                })
                
                for t in tokens1 + tokens2:
                    self.token_usage[t] = self.token_usage.get(t, 0) + 1
        
        print(f"[✓] Loaded {len(self.training_pairs)} training pairs")
    
    def initialize_token_vectors(self):
        """Initialize 82D token vectors."""
        print(f"\n[*] Initializing 82D token vectors...")
        
        for token_id in range(2304):
            base_41d = np.zeros(41)
            for i in range(41):
                if i % 2 == 0:
                    base_41d[i] = np.sin(token_id / (10000 ** (i / 41)))
                else:
                    base_41d[i] = np.cos(token_id / (10000 ** (i / 41)))
            
            influence_41d = base_41d.copy() + np.random.randn(41) * 0.01
            self.token_vectors[token_id] = np.concatenate([base_41d, influence_41d])
        
        print(f"[✓] Initialized {len(self.token_vectors)} token vectors")
    
    def tokens_to_vector(self, token_ids: List[int]) -> np.ndarray:
        """Convert tokens to 82D vector."""
        vectors = [self.token_vectors[tid] for tid in token_ids if 0 <= tid < 2304]
        if not vectors:
            return np.zeros(82)
        return np.mean(vectors, axis=0)
    
    def forward(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Forward pass."""
        hidden = np.tanh(x @ self.W1)
        output = hidden @ self.W2
        return output, hidden
    
    def find_nearest_token(self, output_vector: np.ndarray) -> int:
        """
        Find nearest token to output vector.
        
        Returns token ID of closest match.
        """
        # Normalize
        vec_norm = output_vector / (np.linalg.norm(output_vector) + 1e-8)
        token_norms = self.token_vectors / (
            np.linalg.norm(self.token_vectors, axis=1, keepdims=True) + 1e-8
        )
        
        # Cosine similarity
        similarities = token_norms @ vec_norm
        
        return int(np.argmax(similarities))
    
    def compute_diversity_penalty(self) -> float:
        """
        NEW: Compute penalty for repetitive predictions.
        
        Returns:
            Penalty value (0 = diverse, 1 = all same)
        """
        if len(self.recent_predictions) < 10:
            return 0.0
        
        # Count unique predictions in recent window
        unique_count = len(set(self.recent_predictions[-self.prediction_window:]))
        window_size = min(len(self.recent_predictions), self.prediction_window)
        
        # Diversity score: 1.0 = all unique, 0.0 = all same
        diversity = unique_count / window_size
        
        # Penalty: inverse of diversity
        penalty = 1.0 - diversity
        
        return penalty
    
    def compute_loss(
        self, 
        predicted: np.ndarray, 
        target: np.ndarray,
        predicted_token: int
    ) -> float:
        """
        NEW: Compute loss with diversity penalty.
        
        Total loss = MSE + diversity_weight * diversity_penalty
        """
        # Standard MSE loss
        mse = np.mean((predicted - target) ** 2)
        
        # Track this prediction
        self.recent_predictions.append(predicted_token)
        
        # Diversity penalty
        diversity_penalty = self.compute_diversity_penalty()
        
        # Combined loss
        total_loss = mse + self.diversity_weight * diversity_penalty
        
        return total_loss, mse, diversity_penalty
    
    def backward(
        self, 
        x: np.ndarray, 
        hidden: np.ndarray, 
        output: np.ndarray, 
        target: np.ndarray
    ):
        """Backward pass."""
        d_output = 2 * (output - target) / target.size
        dW2 = np.outer(hidden, d_output)
        d_hidden = (d_output @ self.W2.T) * (1 - hidden ** 2)
        dW1 = np.outer(x, d_hidden)
        
        self.W1 -= self.learning_rate * dW1
        self.W2 -= self.learning_rate * dW2
    
    def train_batch(self, batch: List[Dict]) -> Tuple[float, float, float]:
        """
        Train on batch.
        
        Returns:
            (total_loss, mse_loss, diversity_penalty)
        """
        batch_loss = 0.0
        batch_mse = 0.0
        batch_diversity = 0.0
        
        for pair in batch:
            x = self.tokens_to_vector(pair['tokens1'])
            target = self.tokens_to_vector(pair['tokens2'])
            
            output, hidden = self.forward(x)
            
            # Find predicted token (for diversity tracking)
            predicted_token = self.find_nearest_token(output)
            
            # Compute loss with diversity penalty
            loss, mse, diversity = self.compute_loss(output, target, predicted_token)
            batch_loss += loss
            batch_mse += mse
            batch_diversity += diversity
            
            self.backward(x, hidden, output, target)
        
        return (
            batch_loss / len(batch),
            batch_mse / len(batch),
            batch_diversity / len(batch)
        )
    
    def train(self):
        """Run training loop."""
        print("\n" + "="*60)
        print("TRAINING WITH DIVERSITY PENALTY")
        print("="*60)
        
        total_iterations = 0
        
        for epoch in range(self.epochs):
            epoch_loss = 0.0
            epoch_mse = 0.0
            epoch_diversity = 0.0
            num_batches = 0
            
            np.random.shuffle(self.training_pairs)
            
            for i in range(0, len(self.training_pairs), self.batch_size):
                batch = self.training_pairs[i:i+self.batch_size]
                
                loss, mse, diversity = self.train_batch(batch)
                epoch_loss += loss
                epoch_mse += mse
                epoch_diversity += diversity
                num_batches += 1
                total_iterations += 1
                
                if total_iterations % self.checkpoint_interval == 0:
                    self.save_checkpoint(total_iterations)
            
            avg_loss = epoch_loss / num_batches
            avg_mse = epoch_mse / num_batches
            avg_diversity = epoch_diversity / num_batches
            
            self.losses.append(avg_loss)
            self.diversity_scores.append(avg_diversity)
            
            # Show diversity metric
            unique_recent = len(set(self.recent_predictions[-100:]))
            print(f"Epoch {epoch+1}/{self.epochs} - Loss: {avg_loss:.6f} (MSE: {avg_mse:.6f}, Diversity penalty: {avg_diversity:.3f}) - Unique tokens (last 100): {unique_recent}")
        
        print("\n[✓] Training complete!")
    
    def save_checkpoint(self, iteration: int):
        """Save checkpoint."""
        checkpoint_dir = Path("training/checkpoints")
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        checkpoint_file = checkpoint_dir / f"diverse_checkpoint_{iteration:06d}.npz"
        np.savez(checkpoint_file, W1=self.W1, W2=self.W2, iteration=iteration)
        
        print(f"    [→] Checkpoint saved: {checkpoint_file.name}")
    
    def save_final_model(self):
        """Save final model."""
        print(f"\n[*] Saving final model...")
        
        self.weights_output.parent.mkdir(parents=True, exist_ok=True)
        np.savez(
            self.weights_output,
            W1=self.W1,
            W2=self.W2,
            trained_epochs=self.epochs,
            final_loss=self.losses[-1] if self.losses else 0.0,
            timestamp=datetime.utcnow().isoformat() + 'Z'
        )
        print(f"[✓] Model weights saved: {self.weights_output}")
        
        self.vectors_output.parent.mkdir(parents=True, exist_ok=True)
        np.save(self.vectors_output, self.token_vectors)
        print(f"[✓] Token vectors saved: {self.vectors_output}")
    
    def plot_stats(self):
        """Print training statistics."""
        if not self.losses:
            return
        
        print(f"\n[*] Training Statistics:")
        print(f"    Initial loss: {self.losses[0]:.6f}")
        print(f"    Final loss: {self.losses[-1]:.6f}")
        print(f"    Improvement: {((self.losses[0] - self.losses[-1]) / self.losses[0] * 100):.2f}%")
        
        if self.diversity_scores:
            print(f"    Final diversity penalty: {self.diversity_scores[-1]:.3f}")
            print(f"    (Lower is better - means more diverse predictions)")
        
        # Show prediction distribution
        unique_predictions = len(set(self.recent_predictions))
        total_predictions = len(self.recent_predictions)
        print(f"    Unique tokens predicted: {unique_predictions}/{total_predictions}")
    
    def run(self):
        """Run complete pipeline."""
        print("="*60)
        print("DIVERSE GPU TRAINING - MINIMALLLM 82D")
        print("="*60)
        
        self.load_training_pairs()
        self.initialize_token_vectors()
        self.train()
        self.save_final_model()
        self.plot_stats()
        
        print("\n" + "="*60)
        print("TRAINING COMPLETE")
        print("="*60)


if __name__ == "__main__":
    trainer = DiverseMinimalLLMTrainer(
        pairs_file="training/massive_semantic_pairs.txt",
        weights_output="memory/model_weights.npz",
        vectors_output="tokenizer/token_influence_vectors.npy",
        learning_rate=0.001,
        epochs=200,
        batch_size=32,
        diversity_weight=0.3  # Penalty strength (tune if needed)
    )
    
    trainer.run()