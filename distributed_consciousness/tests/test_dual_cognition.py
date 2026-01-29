#!/usr/bin/env python3
"""
Dual Cognition Test
===================
Run EM field model AND Standard model on same input.
See how they differ - like left brain vs right brain.
"""

import sys
import numpy as np
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from models.minimal_llm_498d import MinimalLLM498D
from tokenizer.text_encoder import ConstraintLatticeEncoder
from tokenizer.text_decoder import TextDecoder

def vector_to_top_tokens(vector, top_k=7):
    """Get top K tokens from vector."""
    top_indices = np.argsort(vector)[-top_k:][::-1]
    return [int(idx) for idx in top_indices]

def dual_cognition_test():
    """Test EM vs Standard on same inputs."""
    
    print("="*70)
    print("DUAL COGNITION: EM FIELD vs STANDARD MODEL")
    print("="*70)
    print()
    
    # Load both models
    print("Loading models...")
    
    # EM Field Model
    em_model = MinimalLLM498D()
    em_weights = np.load("models/minimal_llm_498d_weights_em field.npz")
    em_model.W1 = em_weights['W1']
    em_model.W2 = em_weights['W2']
    em_model.b1 = em_weights['b1']
    em_model.b2 = em_weights['b2']
    print("✅ EM Field Model (cognitive/structure)")
    
    # Standard Model
    std_model = MinimalLLM498D()
    std_weights = np.load("models/emotion_worker_psychology_weights.npz")
    std_model.W1 = std_weights['W1']
    std_model.W2 = std_weights['W2']
    std_model.b1 = std_weights['b1']
    std_model.b2 = std_weights['b2']
    print("✅ Standard Model (emotion/psychology)")
    
    # Load encoder/decoder
    encoder = ConstraintLatticeEncoder()
    decoder = TextDecoder()
    vectors = np.load("tokenizer/token_vectors_498d.npy")
    
    print()
    print("="*70)
    print("Testing different inputs...")
    print("="*70)
    
    # Test inputs
    test_cases = [
        "fire",
        "anxiety", 
        "therapy",
        "stress",
        "help",
        "disorder"
    ]
    
    for word in test_cases:
        print(f"\n{'='*70}")
        print(f"INPUT: '{word}'")
        print("="*70)
        
        # Encode
        tokens = encoder.encode_word(word)
        if not tokens or len(tokens) == 0:
            print("❌ Word not in vocabulary")
            continue
        
        input_vec = vectors[tokens[0]]
        
        # Process through EM model
        em_output, _ = em_model.forward(input_vec)
        em_token_ids = vector_to_top_tokens(em_output, top_k=7)
        em_words = decoder.decode_tokens(em_token_ids)
        
        # Process through Standard model  
        std_output, _ = std_model.forward(input_vec)
        std_token_ids = vector_to_top_tokens(std_output, top_k=7)
        std_words = decoder.decode_tokens(std_token_ids)
        
        # Calculate difference
        similarity = np.dot(em_output, std_output) / (
            np.linalg.norm(em_output) * np.linalg.norm(std_output)
        )
        difference = 1.0 - similarity
        
        # Display results
        print(f"\n🧠 EM FIELD (Cognitive/Structure):")
        print(f"   {em_words}")
        
        print(f"\n💙 STANDARD (Emotion/Probability):")
        print(f"   {std_words}")
        
        print(f"\n📊 Comparison:")
        print(f"   Similarity: {similarity:.3f}")
        print(f"   Difference: {difference:.3f}")
        
        if difference < 0.2:
            print(f"   → Models AGREE (similar interpretation)")
        elif difference < 0.5:
            print(f"   → Models DIVERGE (moderate difference)")
        else:
            print(f"   → Models CONFLICT (very different views)")
    
    print("\n" + "="*70)
    print("✅ DUAL COGNITION TEST COMPLETE")
    print("="*70)
    print()
    print("Insights:")
    print("  - EM Field: structure/semantics/logic")
    print("  - Standard: emotion/probability/feeling")
    print("  - Both create unified consciousness")
    print("  - Difference = 'debate' between perspectives")

if __name__ == "__main__":
    dual_cognition_test()
