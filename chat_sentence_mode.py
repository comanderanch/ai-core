#!/usr/bin/env python3
"""
AI-Core: Sentence-level chat (bypasses word tokenization)
"""
import sys
import numpy as np
from pathlib import Path

sys.path.append('models')
sys.path.append('tokenizer')

from minimal_llm_498d import MinimalLLM498D
from text_encoder import ConstraintLatticeEncoder  
from text_decoder import TextDecoder

class SentenceLevelChat:
    def __init__(self, weights_file="models/minimal_llm_498d_weights_em field.npz"):
        print("🔥 Initializing Sentence-Level AI-Core...")
        
        self.model = MinimalLLM498D()
        data = np.load(weights_file)
        self.model.W1, self.model.W2 = data['W1'], data['W2']
        self.model.b1, self.model.b2 = data['b1'], data['b2']
        
        self.encoder = ConstraintLatticeEncoder()
        self.decoder = TextDecoder()
        self.vectors = np.load("tokenizer/token_vectors_498d.npy")
        
        print("✅ Ready!\n")
    
    def sentence_to_vector(self, sentence):
        """Convert sentence to single 498D vector (average of all words)."""
        words = sentence.lower().split()
        vectors = []
        
        for word in words:
            try:
                token_ids = self.encoder.encode_word(word)
                if token_ids and len(token_ids) > 0:
                    vectors.append(self.vectors[token_ids[0]])
            except:
                pass
        
        if not vectors:
            return None
        
        # Average all word vectors
        return np.mean(vectors, axis=0)
    
    def generate_response(self, user_input):
        """Generate response from user input."""
        # Encode input
        input_vec = self.sentence_to_vector(user_input)
        
        if input_vec is None:
            return "[Unable to understand input]"
        
        # Single forward pass
        output = self.model.forward(input_vec)
        if isinstance(output, tuple):
            output = output[0]
        
        # Find nearest tokens and decode
        distances = np.linalg.norm(self.vectors - output, axis=1)
        top_5 = np.argsort(distances)[:5]
        
        words = []
        for token_id in top_5:
            word = self.decoder.decode_token(token_id)
            if word and word not in words:
                words.append(word)
        
        return " ".join(words[:3])  # Return top 3 unique words
    
    def chat(self):
        print("="*60)
        print("AI-CORE SENTENCE-LEVEL CHAT")
        print("="*60)
        print("Type /quit to exit\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input == "/quit":
                    print("👋 Goodbye!")
                    break
                
                response = self.generate_response(user_input)
                print(f"AI: {response}\n")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

if __name__ == "__main__":
    chat = SentenceLevelChat()
    chat.chat()
