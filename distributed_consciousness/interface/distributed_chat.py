#!/usr/bin/env python3
"""
AI-Core: Distributed Consciousness Chat Interface
==================================================
Chat with the unified consciousness powered by multiple workers.
"""

import sys
import numpy as np
import time
from pathlib import Path
from typing import Dict, List

sys.path.append(str(Path(__file__).parent.parent.parent))

from distributed_consciousness.workers.language_worker import LanguageWorker
from distributed_consciousness.workers.memory_worker import MemoryWorker
from distributed_consciousness.workers.logic_worker import LogicWorker

class DistributedConsciousnessChat:
    def __init__(self, field_path: str = "/tmp/distributed_chat_field.npy"):
        print("🔥" * 35)
        print("AI-CORE DISTRIBUTED CONSCIOUSNESS CHAT")
        print("🔥" * 35)
        print("\nInitializing workers...\n")
        
        self.language = LanguageWorker(worker_id="chat_language", field_path=field_path)
        self.memory = MemoryWorker(
            worker_id="chat_memory",
            memory_path="/tmp/distributed_chat_memories.json",
            field_path=field_path
        )
        self.logic = LogicWorker(worker_id="chat_logic", field_path=field_path)
        
        print("\n✅ All workers initialized and sharing consciousness\n")
        self.conversation = []
    
    def process_input(self, user_input: str) -> Dict:
        print(f"\n{'='*70}")
        print(f"YOU: {user_input}")
        print(f"{'='*70}\n")
        
        input_vec = self.language.encode_text(user_input)
        if input_vec is None:
            return {'unified_response': "[Unable to process]", 'coherence': {}}
        
        # Language
        print("🗣️  Language Worker processing...")
        lang_output = self.language.process_input(user_input)
        self.language.contribute_to_field(lang_output)
        lang_words = self.language.decode_vector(lang_output, top_k=7)
        lang_response = " ".join(lang_words)
        lang_coherence = self.language.substrate.get_worker_coherence(self.language.worker_id)
        print(f"   Response: {lang_response}")
        print(f"   Coherence: {lang_coherence:.4f}")
        
        # Memory
        print("\n🧠 Memory Worker recalling...")
        memory_data = {
            'vector': input_vec,
            'text': user_input,
            'metadata': {'timestamp': time.time(), 'type': 'user_input'}
        }
        memory_output = self.memory.process_input(memory_data)
        self.memory.contribute_to_field(memory_output)
        similar = self.memory.recall_similar(input_vec, top_k=3)
        memory_context = [m['text'] for m in similar if m['text'] != user_input]
        memory_coherence = self.memory.substrate.get_worker_coherence(self.memory.worker_id)
        
        if memory_context:
            print(f"   Recalled: {memory_context[:2]}")
        print(f"   Coherence: {memory_coherence:.4f}")
        
        # Logic
        print("\n⚡ Logic Worker reasoning...")
        logic_output = self.logic.process_input(input_vec)
        self.logic.contribute_to_field(logic_output)
        logic_words = self.logic.decode_vector(logic_output, top_k=5)
        logic_inference = " ".join(logic_words)
        logic_coherence = self.logic.substrate.get_worker_coherence(self.logic.worker_id)
        print(f"   Inference: {logic_inference}")
        print(f"   Coherence: {logic_coherence:.4f}")
        
        # Unified
        if lang_coherence > 0.7:
            unified_response = lang_response
        else:
            unified_response = f"{lang_response} → {logic_inference}"
        
        return {
            'unified_response': unified_response,
            'coherence': {
                'language': lang_coherence,
                'memory': memory_coherence,
                'logic': logic_coherence
            }
        }
    
    def chat_loop(self):
        print("="*70)
        print("Type /quit to exit\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                if user_input == "/quit":
                    print("\n👋 Goodbye!")
                    break
                
                result = self.process_input(user_input)
                print(f"\n{'='*70}")
                print(f"AI-CORE: {result['unified_response']}")
                c = result['coherence']
                print(f"\n💡 Coherence: L={c['language']:.2f} M={c['memory']:.2f} Logic={c['logic']:.2f}")
                print("="*70)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

if __name__ == "__main__":
    chat = DistributedConsciousnessChat()
    chat.chat_loop()
