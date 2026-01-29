#!/usr/bin/env python3
"""
Communication Integration Bot - The Consciousness Layer
"""

import sys
import numpy as np
from pathlib import Path

sys.path.append(str(Path.home() / 'ai-core'))

from models.minimal_llm_498d import MinimalLLM498D
from tokenizer.text_encoder import ConstraintLatticeEncoder
from tokenizer.text_decoder import TextDecoder

class CommunicationBot:
    def __init__(self):
        print("🧠 Initializing Communication Integration Bot...")
        
        self.encoder = ConstraintLatticeEncoder()
        self.decoder = TextDecoder()
        self.vectors = np.load('tokenizer/token_vectors_498d.npy')
        
        self.workers = {}
        self._load_workers()
        
        print("✅ Ready!\n")
    
    def _load_workers(self):
        """Load all cognitive models"""
        
        # EM Field
        em_model = MinimalLLM498D()
        em_data = np.load('models/minimal_llm_498d_weights_em field.npz')
        em_model.W1, em_model.W2 = em_data['W1'], em_data['W2']
        em_model.b1, em_model.b2 = em_data['b1'], em_data['b2']
        self.workers['em_field'] = {'model': em_model, 'name': 'EM Field', 'color': '\033[94m'}
        
        # Standard
        std_model = MinimalLLM498D()
        std_data = np.load('models/minimal_llm_498d_weights_standard.npz')
        std_model.W1, std_model.W2 = std_data['W1'], std_data['W2']
        std_model.b1, std_model.b2 = std_data['b1'], std_data['b2']
        self.workers['standard'] = {'model': std_model, 'name': 'Standard', 'color': '\033[92m'}
        
        # Emotion
        emo_model = MinimalLLM498D()
        emo_data = np.load('models/emotion_worker_psychology_weights.npz')
        emo_model.W1, emo_model.W2 = emo_data['W1'], emo_data['W2']
        emo_model.b1, emo_model.b2 = emo_data['b1'], emo_data['b2']
        self.workers['emotion'] = {'model': emo_model, 'name': 'Emotion', 'color': '\033[95m'}
        
        print("Loaded: EM Field, Standard, Emotion")
    
    def encode_text(self, text):
        """Encode text to 498D vector"""
        words = text.lower().split()
        vecs = []
        
        for word in words:
            try:
                tokens = self.encoder.encode_word(word)
                if tokens and len(tokens) > 0:
                    vecs.append(self.vectors[tokens[0]])
            except:
                pass
        
        if not vecs:
            return np.zeros(498)
        return np.mean(vecs, axis=0)
    
    def decode_vector(self, vec, top_k=5):
        """Decode 498D vector to words"""
        distances = np.linalg.norm(self.vectors - vec, axis=1)
        top_indices = np.argsort(distances)[:top_k]
        words = [self.decoder.decode_token(int(idx)) for idx in top_indices if self.decoder.decode_token(int(idx))]
        return ' '.join(words[:top_k])
    
    def process_input(self, user_input):
        """Main processing"""
        
        reset = '\033[0m'
        
        print(f"\n{'='*70}")
        print(f"INPUT: {user_input}")
        print(f"{'='*70}\n")
        
        input_vec = self.encode_text(user_input)
        
        responses = {}
        for name, worker in self.workers.items():
            output, _ = worker['model'].forward(input_vec)
            response_text = self.decode_vector(output, top_k=5)
            responses[name] = {'vector': output, 'text': response_text}
            
            color = worker['color']
            worker_name = worker['name']
            print(f"{color}{worker_name:12}{reset}: {response_text}")
        
        print(f"\n{'─'*70}")
        print("DIVERGENCE ANALYSIS:")
        print(f"{'─'*70}")
        
        em_vec = responses['em_field']['vector']
        std_vec = responses['standard']['vector']
        emo_vec = responses['emotion']['vector']
        
        def calc_div(v1, v2):
            sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            return 1 - sim
        
        em_std = calc_div(em_vec, std_vec)
        em_emo = calc_div(em_vec, emo_vec)
        std_emo = calc_div(std_vec, emo_vec)
        
        print(f"EM vs Standard: {em_std:.2%}")
        print(f"EM vs Emotion:  {em_emo:.2%}")
        print(f"Std vs Emotion: {std_emo:.2%}")
        
        unified = (em_vec * 0.4 + std_vec * 0.3 + emo_vec * 0.3)
        unified_text = self.decode_vector(unified, top_k=7)
        
        print(f"\n{'─'*70}")
        print(f"UNIFIED RESPONSE: {unified_text}")
        print(f"{'='*70}\n")
        
        if max(em_std, em_emo, std_emo) > 0.5:
            print("⚡ SIGNIFICANT DEBATE (>50% divergence)\n")

def main():
    print("\n🔥 COMMUNICATION INTEGRATION BOT 🔥\n")
    
    bot = CommunicationBot()
    
    tests = ["anxiety disorder", "fire", "therapy", "help"]
    
    for test in tests:
        bot.process_input(test)
        input("Press Enter...")

if __name__ == "__main__":
    main()
