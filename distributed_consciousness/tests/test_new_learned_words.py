#!/usr/bin/env python3
"""
Test Dual Cognition with Newly Learned Words
"""

import sys
import numpy as np
from pathlib import Path

sys.path.append(str(Path.home() / 'ai-core'))

from models.minimal_llm_498d import MinimalLLM498D
from tokenizer.text_encoder import ConstraintLatticeEncoder
from tokenizer.text_decoder import TextDecoder

def test_learned_words():
    print("\n" + "="*70)
    print("TESTING NEWLY LEARNED WORDS")
    print("="*70)
    print()
    
    # Load models
    em_model = MinimalLLM498D()
    em_data = np.load('models/minimal_llm_498d_weights_em field.npz')
    em_model.W1, em_model.W2 = em_data['W1'], em_data['W2']
    em_model.b1, em_model.b2 = em_data['b1'], em_data['b2']
    
    emo_model = MinimalLLM498D()
    emo_data = np.load('models/emotion_worker_psychology_weights.npz')
    emo_model.W1, emo_model.W2 = emo_data['W1'], emo_data['W2']
    emo_model.b1, emo_model.b2 = emo_data['b1'], emo_data['b2']
    
    # Load tokenizer
    encoder = ConstraintLatticeEncoder()
    decoder = TextDecoder()
    vectors = np.load('tokenizer/token_vectors_498d.npy')
    
    print(f"Loaded {len(vectors)} token vectors")
    print()
    
    # Test newly learned words
    new_words = ['neuroscience', 'neuroplasticity', 'synapse', 'cognition', 'thermodynamics']
    
    reset = '\033[0m'
    
    for word in new_words:
        print(f"{'='*70}")
        print(f"WORD: {word}")
        print(f"{'='*70}")
        
        # Encode
        tokens = encoder.encode_word(word)
        if not tokens or len(tokens) == 0:
            print(f"❌ Word not encoded!\n")
            continue
        
        token_id = tokens[0]
        if token_id >= len(vectors):
            print(f"❌ Token {token_id} out of range!\n")
            continue
        
        input_vec = vectors[token_id]
        
        # Process through both models
        em_output, _ = em_model.forward(input_vec)
        emo_output, _ = emo_model.forward(input_vec)
        
        # Decode
        em_words = []
        emo_words = []
        
        distances_em = np.linalg.norm(vectors - em_output, axis=1)
        top_em = np.argsort(distances_em)[:5]
        for idx in top_em:
            w = decoder.decode_token(int(idx))
            if w:
                em_words.append(w)
        
        distances_emo = np.linalg.norm(vectors - emo_output, axis=1)
        top_emo = np.argsort(distances_emo)[:5]
        for idx in top_emo:
            w = decoder.decode_token(int(idx))
            if w:
                emo_words.append(w)
        
        # Calculate divergence
        sim = np.dot(em_output, emo_output) / (np.linalg.norm(em_output) * np.linalg.norm(emo_output))
        div = 1 - sim
        
        print(f"\n\033[94mEM Field:\033[0m     {' '.join(em_words)}")
        print(f"\033[95mEmotion:\033[0m      {' '.join(emo_words)}")
        print(f"\nDivergence: {div:.2%}")
        
        if div > 0.5:
            print("⚡ SIGNIFICANT DEBATE!")
        
        print()
    
    print("="*70)
    print("✅ TEST COMPLETE")
    print("="*70)

if __name__ == "__main__":
    test_learned_words()
