#!/usr/bin/env python3
"""
Train Emotion Worker on psychology semantic pairs.
"""

import sys
import numpy as np
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from models.minimal_llm_498d import MinimalLLM498D
from tokenizer.text_encoder import ConstraintLatticeEncoder

def load_psychology_pairs():
    """Load psychology semantic pairs."""
    pairs = []
    
    files = [
        "training_data/psychology_pairs_cognitive.txt",
        "training_data/psychology_pairs_book.txt"
    ]
    
    for file in files:
        if Path(file).exists():
            with open(file, 'r') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        w1, w2 = parts[0], parts[1]
                        pairs.append((w1, w2))
    
    print(f"Loaded {len(pairs)} psychology pairs")
    return pairs

def train_emotion_model(pairs, epochs=200):
    """Train emotion model."""
    print("="*70)
    print("TRAINING EMOTION WORKER ON PSYCHOLOGY")
    print("="*70)
    print()
    
    model = MinimalLLM498D()
    encoder = ConstraintLatticeEncoder()
    vectors = np.load("tokenizer/token_vectors_498d.npy")
    
    print(f"Model: {model.W1.shape[0]}D → {model.W1.shape[1]}D → {model.W2.shape[0]}D")
    print(f"Training pairs: {len(pairs)}")
    print()
    
    # Encode pairs
    print("Encoding pairs...")
    training_data = []
    
    for w1, w2 in pairs:
        try:
            tokens1 = encoder.encode_word(w1)
            tokens2 = encoder.encode_word(w2)
            
            if tokens1 and tokens2 and len(tokens1) > 0 and len(tokens2) > 0:
                vec1 = vectors[tokens1[0]]
                vec2 = vectors[tokens2[0]]
                training_data.append((vec1, vec2))
        except:
            pass
    
    print(f"Encoded {len(training_data)} pairs")
    print()
    print("Training...")
    print()
    
    for epoch in range(epochs):
        total_loss = 0
        
        for input_vec, target_vec in training_data:
            # Forward pass (returns output AND cache)
            output, cache = model.forward(input_vec)
            
            # Loss
            loss = np.mean((output - target_vec) ** 2)
            total_loss += loss
            
            # Backward pass with cache
            dW1, db1, dW2, db2 = model.backward(cache, target_vec, output)
            
            # Update weights
            model.W1 -= model.learning_rate * dW1
            model.b1 -= model.learning_rate * db1
            model.W2 -= model.learning_rate * dW2
            model.b2 -= model.learning_rate * db2
        
        avg_loss = total_loss / len(training_data)
        
        if epoch % 10 == 0:
            print(f"Epoch {epoch:3d}: Loss = {avg_loss:.6f}")
    
    print()
    print("="*70)
    print("✅ TRAINING COMPLETE")
    print(f"   Final loss: {avg_loss:.6f}")
    print("="*70)
    
    # Save
    output_file = "models/emotion_worker_psychology_weights.npz"
    np.savez(output_file, W1=model.W1, W2=model.W2, b1=model.b1, b2=model.b2)
    
    print(f"\n💾 Saved: {output_file}")
    
    return model, avg_loss

if __name__ == "__main__":
    pairs = load_psychology_pairs()
    model, final_loss = train_emotion_model(pairs, epochs=200)
    
    print("\n🧠💙 Emotion worker trained on psychology!")
