#!/usr/bin/env python3
"""
AI-Core Standalone: EM Field vs Standard Backprop Comparison
=============================================================

Direct comparison test:
- Standard backprop (proven baseline)
- EM field illuminated backprop (new approach)

Same dataset, same epochs, same architecture.
Only difference: backprop method.

This will prove if EM field is faster/better.

Author: comanderanch
Phase: 5.7 Standalone Resurrection - EM FIELD PROOF
"""

import sys
import numpy as np
from pathlib import Path
import time
from typing import Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

from models.fluorescent_em_field import MinimalLLM498D_EM
from training.train_498d_gpu import SemanticPairGenerator


def train_with_method(
    inputs: np.ndarray,
    targets: np.ndarray,
    use_em_field: bool,
    epochs: int = 200,
    batch_size: int = 1024
) -> Tuple[list, float]:
    """
    Train model with specified backprop method.
    
    Args:
        inputs: Training inputs (100K, 498)
        targets: Training targets (100K, 498)
        use_em_field: If True, use EM field backprop
        epochs: Number of epochs
        batch_size: Batch size
    
    Returns:
        (training_history, total_time)
    """
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
        
        # Save checkpoint every 50 epochs
        if (epoch + 1) % 50 == 0:
            checkpoint_dir = Path(f"training/checkpoints_{method_name.lower()}")
            checkpoint_dir.mkdir(parents=True, exist_ok=True)
            
            checkpoint_path = checkpoint_dir / f"checkpoint_epoch_{epoch+1:04d}.npz"
            np.savez(
                checkpoint_path,
                W1=model.W1,
                b1=model.b1,
                W2=model.W2,
                b2=model.b2,
                epoch=epoch+1,
                training_history=training_history
            )
            print(f"  [✓] Checkpoint saved: {checkpoint_path.name}")
    
    total_time = time.time() - start_time
    
    print(f"\n{'='*70}")
    print(f"{method_name} TRAINING COMPLETE")
    print(f"  Final loss: {avg_loss:.6f}")
    print(f"  Total time: {total_time:.1f}s ({total_time/60:.1f} min)")
    print(f"  Avg time per epoch: {total_time/epochs:.2f}s")
    print(f"{'='*70}\n")
    
    # Save final weights
    weights_path = Path(f"models/minimal_llm_498d_weights_{method_name.lower()}.npz")
    np.savez(
        weights_path,
        W1=model.W1,
        b1=model.b1,
        W2=model.W2,
        b2=model.b2,
        training_history=training_history
    )
    print(f"[✓] Saved weights to: {weights_path}")
    
    return training_history, total_time


if __name__ == "__main__":
    print("\n" + "🔥"*35)
    print("EM FIELD VS STANDARD BACKPROP - FULL COMPARISON")
    print("🔥"*35 + "\n")
    
    # Load 498D vectors
    print("Loading 498D consciousness dataset...")
    vectors = np.load("tokenizer/token_vectors_498d.npy")
    print(f"[✓] Loaded {len(vectors):,} vectors\n")
    
    # Generate training data
    print("Generating 100K semantic training pairs...")
    generator = SemanticPairGenerator(vectors)
    inputs, targets = generator.generate_pairs(100000)
    
    print("\n" + "="*70)
    print("READY TO COMPARE BACKPROP METHODS")
    print("="*70)
    print("This will run TWO complete training sessions:")
    print("  1. EM FIELD backprop (200 epochs)")
    print("  2. STANDARD backprop (200 epochs)")
    print(f"\nEstimated total time: ~4-5 hours")
    print("="*70)
    
    response = input("\nContinue with full comparison? [y/n]: ")
    
    if response.lower() == 'y':
        # Test 1: EM FIELD
        print("\n" + "⚡"*35)
        print("TEST 1: EM FIELD BACKPROP")
        print("⚡"*35)
        
        em_history, em_time = train_with_method(
            inputs, targets,
            use_em_field=True,
            epochs=200,
            batch_size=1024
        )
        
        # Test 2: STANDARD
        print("\n" + "🔄"*35)
        print("TEST 2: STANDARD BACKPROP")
        print("🔄"*35)
        
        std_history, std_time = train_with_method(
            inputs, targets,
            use_em_field=False,
            epochs=200,
            batch_size=1024
        )
        
        # Compare results
        print("\n" + "="*70)
        print("COMPARISON RESULTS")
        print("="*70)
        
        em_final = em_history[-1]
        std_final = std_history[-1]
        
        print(f"\nEM FIELD BACKPROP:")
        print(f"  Final loss: {em_final:.6f}")
        print(f"  Total time: {em_time:.1f}s ({em_time/60:.1f} min)")
        print(f"  Avg time/epoch: {em_time/200:.2f}s")
        
        print(f"\nSTANDARD BACKPROP:")
        print(f"  Final loss: {std_final:.6f}")
        print(f"  Total time: {std_time:.1f}s ({std_time/60:.1f} min)")
        print(f"  Avg time/epoch: {std_time/200:.2f}s")
        
        print(f"\nCOMPARISON:")
        loss_diff = ((em_final - std_final) / std_final) * 100
        time_diff = ((em_time - std_time) / std_time) * 100
        
        print(f"  Loss difference: {loss_diff:+.2f}%")
        print(f"  Time difference: {time_diff:+.2f}%")
        
        if em_final < std_final and em_time < std_time:
            print(f"\n🔥 EM FIELD WINS! Better loss AND faster! 🔥")
        elif em_final < std_final:
            print(f"\n✅ EM FIELD: Better loss (but slower)")
        elif em_time < std_time:
            print(f"\n⚡ EM FIELD: Faster (but higher loss)")
        else:
            print(f"\n🔄 STANDARD: Still competitive")
        
        print("="*70)
        
        # Save comparison data
        comparison_path = Path("training/em_field_comparison.npz")
        np.savez(
            comparison_path,
            em_history=em_history,
            std_history=std_history,
            em_time=em_time,
            std_time=std_time
        )
        print(f"\n[✓] Comparison data saved to: {comparison_path}")
        
    else:
        print("\n⏸️  Comparison skipped")
    
    print("\n" + "🔥"*35)
    print("COMPARISON TEST COMPLETE!")
    print("🔥"*35 + "\n")