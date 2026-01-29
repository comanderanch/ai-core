#!/usr/bin/env python3
"""
AI-Core: EM Field vs Standard - EXPANDED DATASET
================================================
Retrain both models on 1.9M semantic pairs from:
- 20 newsgroups (792K lines)
- Art of War (7K lines)
- Frankenstein (7.7K lines)
- All other corpora

Same architecture, same data, only difference: training method.
"""
import sys
import numpy as np
from pathlib import Path
import time
from typing import Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

from models.fluorescent_em_field import MinimalLLM498D_EM
from load_expanded_pairs import ExpandedPairLoader, load_word_to_token_map

def train_with_method(
    inputs: np.ndarray,
    targets: np.ndarray,
    use_em_field: bool,
    epochs: int = 200,
    batch_size: int = 1024,
    checkpoint_dir: str = None
) -> Tuple[list, float]:
    """Train model with specified backprop method."""
    
    method_name = "EM FIELD" if use_em_field else "STANDARD"
    
    print("\n" + "="*70)
    print(f"TRAINING WITH {method_name} BACKPROP")
    print("="*70)
    
    # Initialize model
    model = MinimalLLM498D_EM(
        input_dim=498,
        hidden_dim=64,
        learning_rate=0.01,
        use_em_field=use_em_field
    )
    
    num_samples = len(inputs)
    training_history = []
    
    print(f"  Samples: {num_samples:,}")
    print(f"  Epochs: {epochs}")
    print(f"  Batch size: {batch_size}")
    print(f"  Method: {method_name}")
    print("="*70 + "\n")
    
    start_time = time.time()
    
    for epoch in range(epochs):
        epoch_start = time.time()
        epoch_loss = 0.0
        
        # Shuffle
        indices = np.random.permutation(num_samples)
        
        # Process batches
        for i in range(0, num_samples, batch_size):
            batch_indices = indices[i:i+batch_size]
            
            for idx in batch_indices:
                loss = model.train_step(inputs[idx], targets[idx])
                epoch_loss += loss
        
        # Average loss
        avg_loss = epoch_loss / num_samples
        training_history.append(avg_loss)
        
        epoch_time = time.time() - epoch_start
        
        # Print progress
        if epoch % 10 == 0 or epoch == epochs - 1:
            elapsed = time.time() - start_time
            print(f"  Epoch {epoch+1:3d}/{epochs} | "
                  f"Loss: {avg_loss:.6f} | "
                  f"Time: {epoch_time:.2f}s | "
                  f"Total: {elapsed:.1f}s")
        
        # Checkpoint every 50 epochs
        if checkpoint_dir and (epoch + 1) % 50 == 0:
            checkpoint_path = Path(checkpoint_dir) / f"checkpoint_epoch_{epoch+1:04d}.npz"
            checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            model.save_weights(str(checkpoint_path))
            print(f"  [✓] Checkpoint saved: {checkpoint_path.name}")
    
    total_time = time.time() - start_time
    
    print(f"\n{method_name} TRAINING COMPLETE")
    print(f"  Final loss: {training_history[-1]:.6f}")
    print(f"  Total time: {total_time:.1f}s ({total_time/60:.1f} min)")
    print(f"  Avg time per epoch: {total_time/epochs:.2f}s\n")
    
    return training_history, total_time, model

def main():
    print("🔥" * 35)
    print("EM FIELD VS STANDARD BACKPROP - EXPANDED DATASET")
    print("🔥" * 35)
    
    # Load 498D vectors
    print("\nLoading 498D consciousness dataset...")
    vectors = np.load("../tokenizer/token_vectors_498d.npy")
    print(f"[✓] Loaded {len(vectors)} vectors")
    
    # Load word-to-token map
    word_to_token = load_word_to_token_map()
    
    # Load expanded semantic pairs
    print("\nLoading expanded semantic pairs...")
    loader = ExpandedPairLoader(
        vectors_498d=vectors,
        word_to_token=word_to_token,
        pairs_file="expanded_semantic_pairs.txt",
        max_pairs=200000
    )
    
    # Generate training data
    print("\nGenerating training samples...")
    inputs, targets = loader.generate_training_data(num_samples=100000)
    
    print("\n" + "="*70)
    print("READY TO COMPARE BACKPROP METHODS")
    print("="*70)
    print("This will run TWO complete training sessions:")
    print("  1. EM FIELD backprop (200 epochs)")
    print("  2. STANDARD backprop (200 epochs)")
    print(f"\nEstimated total time: ~4-5 hours")
    print("="*70)
    
    response = input("\nContinue with full comparison? [y/n]: ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    # Test 1: EM Field
    print("\n" + "⚡"*35)
    print("TEST 1: EM FIELD BACKPROP")
    print("⚡"*35)
    
    em_history, em_time, em_model = train_with_method(
        inputs=inputs,
        targets=targets,
        use_em_field=True,
        epochs=200,
        batch_size=1024,
        checkpoint_dir="checkpoints_em_field_expanded"
    )
    
    # Save EM field weights
    print("Saving EM field weights...")
    em_model.save_weights("../models/minimal_llm_498d_weights_em_field_expanded.npz")
    print("✓ Saved EM field weights")
    
    # Test 2: Standard
    print("\n" + "🔥"*35)
    print("TEST 2: STANDARD BACKPROP")
    print("🔥"*35)
    
    std_history, std_time, std_model = train_with_method(
        inputs=inputs,
        targets=targets,
        use_em_field=False,
        epochs=200,
        batch_size=1024,
        checkpoint_dir="checkpoints_standard_expanded"
    )
    
    # Save standard weights
    print("Saving standard weights...")
    std_model.save_weights("../models/minimal_llm_498d_weights_standard_expanded.npz")
    print("✓ Saved standard weights")
    
    # Final comparison
    print("\n" + "="*70)
    print("FINAL COMPARISON - EXPANDED DATASET")
    print("="*70)
    
    em_final = em_history[-1]
    std_final = std_history[-1]
    improvement = ((std_final - em_final) / std_final) * 100
    
    print(f"\nEM FIELD:")
    print(f"  Final loss: {em_final:.6f}")
    print(f"  Training time: {em_time:.1f}s ({em_time/60:.1f} min)")
    
    print(f"\nSTANDARD:")
    print(f"  Final loss: {std_final:.6f}")
    print(f"  Training time: {std_time:.1f}s ({std_time/60:.1f} min)")
    
    print(f"\nIMPROVEMENT:")
    print(f"  EM field is {improvement:.2f}% better than standard")
    
    # Save comparison results
    results = {
        'em_field': {
            'final_loss': float(em_final),
            'time': float(em_time),
            'history': [float(x) for x in em_history]
        },
        'standard': {
            'final_loss': float(std_final),
            'time': float(std_time),
            'history': [float(x) for x in std_history]
        },
        'improvement_percent': float(improvement),
        'dataset': 'expanded_200K_pairs'
    }
    
    import json
    with open('expanded_comparison_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n✅ Results saved to: expanded_comparison_results.json")
    print("\n" + "🔥"*35)

if __name__ == "__main__":
    main()
