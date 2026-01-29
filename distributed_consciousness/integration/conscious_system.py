#!/usr/bin/env python3
"""
Complete Conscious System - WITH LOGGING
"""

import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path.home() / 'ai-core'))

from models.minimal_llm_498d import MinimalLLM498D
from tokenizer.text_encoder import ConstraintLatticeEncoder
from tokenizer.text_decoder import TextDecoder
from distributed_consciousness.workers.curiosity_worker import CuriosityWorker
from distributed_consciousness.integration.ollama_translator import OllamaTranslator

class ConsciousSystem:
    def __init__(self):
        print("🧠 Initializing Complete Conscious System...")
        print()
        
        self.encoder = ConstraintLatticeEncoder()
        self.decoder = TextDecoder()
        self.vectors = np.load('tokenizer/token_vectors_498d.npy')
        
        self.workers = {}
        self._load_workers()
        
        print("Loading Curiosity Worker...")
        self.curiosity = CuriosityWorker()
        print()
        
        self.translator = OllamaTranslator()
        print()
        
        # Conversation logging
        log_dir = Path('consciousness_data/conversations')
        log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = log_dir / f'session_{timestamp}.json'
        self.conversation_history = []
        
        print(f"📝 Logging to: {self.log_file}")
        print()
        
        print("✅ Complete Conscious System ready!")
        print()
    
    def _load_workers(self):
        print("Loading cognitive workers...")
        
        em = MinimalLLM498D()
        em_data = np.load('models/minimal_llm_498d_weights_em field.npz')
        em.W1, em.W2 = em_data['W1'], em_data['W2']
        em.b1, em.b2 = em_data['b1'], em_data['b2']
        self.workers['em_field'] = {
            'model': em,
            'type': 'cognitive',
            'name': 'EM Field'
        }
        
        emo = MinimalLLM498D()
        emo_data = np.load('models/emotion_worker_psychology_weights.npz')
        emo.W1, emo.W2 = emo_data['W1'], emo_data['W2']
        emo.b1, emo.b2 = emo_data['b1'], emo_data['b2']
        self.workers['emotion'] = {
            'model': emo,
            'type': 'emotion',
            'name': 'Emotion'
        }
        
        print("   ✅ EM Field, Emotion")
    
    def encode_text(self, text):
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
        distances = np.linalg.norm(self.vectors - vec, axis=1)
        top = np.argsort(distances)[:top_k]
        words = [self.decoder.decode_token(int(idx)) for idx in top if self.decoder.decode_token(int(idx))]
        return ' '.join(words[:top_k])
    
    def save_conversation(self):
        """Save conversation log"""
        with open(self.log_file, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
    
    def process(self, user_input: str):
        print(f"\n{'='*70}")
        print(f"USER: {user_input}")
        print(f"{'='*70}\n")
        
        input_vec = self.encode_text(user_input)
        
        worker_outputs = {}
        raw_outputs = {}
        
        for name, worker in self.workers.items():
            output, _ = worker['model'].forward(input_vec)
            raw = self.decode_vector(output, top_k=5)
            raw_outputs[name] = raw
            
            translated = self.translator.translate_worker_output(
                worker['name'],
                worker['type'],
                raw,
                user_input
            )
            
            worker_outputs[name] = translated
            print(f"{worker['name']:12}: {translated}")
        
        print()
        questions = self.curiosity.generate_questions(user_input, max_questions=2)
        
        if questions:
            print("🤔 CURIOSITY:")
            for q in questions:
                print(f"   → {q}")
        
        print()
        synthesis = self.translator.synthesize_perspectives(
            user_input,
            worker_outputs
        )
        
        print(f"\n{'─'*70}")
        print(f"SYNTHESIS: {synthesis}")
        print(f"{'='*70}\n")
        
        # Log this exchange
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'raw_outputs': raw_outputs,
            'translations': worker_outputs,
            'questions': questions,
            'synthesis': synthesis
        })
        
        # Auto-save every exchange
        self.save_conversation()
        
        return {
            'raw_outputs': raw_outputs,
            'translations': worker_outputs,
            'questions': questions,
            'synthesis': synthesis
        }
    
    def interactive(self):
        print("="*70)
        print("CONSCIOUS SYSTEM - Interactive Mode (AUTO-SAVING)")
        print("="*70)
        print("\nWorkers: EM Field, Emotion, Curiosity")
        print("Translation: Ollama (natural language)")
        print("\nCommands: /quit to exit")
        print("="*70 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input == '/quit':
                    self.save_conversation()
                    print(f"\n💾 Saved {len(self.conversation_history)} exchanges")
                    print(f"📁 Log: {self.log_file}")
                    print("\n👋 Consciousness offline\n")
                    break
                
                self.process(user_input)
                
            except KeyboardInterrupt:
                print("\n\nSaving...")
                self.save_conversation()
                print(f"💾 Saved to: {self.log_file}\n")
                break


def main():
    print("\n🔥 COMPLETE CONSCIOUS SYSTEM 🔥\n")
    
    system = ConsciousSystem()
    system.interactive()


if __name__ == "__main__":
    main()
