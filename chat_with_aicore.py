#!/usr/bin/env python3
"""
AI-Core: Conversational Interface
Uses EM field trained weights for semantic generation
"""
import sys
import numpy as np
from pathlib import Path

sys.path.append('models')
sys.path.append('tokenizer')

from minimal_llm_498d import MinimalLLM498D
from text_encoder import ConstraintLatticeEncoder
from text_decoder import TextDecoder

class AICoreChat:
    def __init__(self, weights_file="models/minimal_llm_498d_weights_em field.npz"):
        print("🔥 Initializing AI-Core Chat Interface...")
        print()
        
        # Load model with EM weights
        self.model = MinimalLLM498D()
        data = np.load(weights_file)
        self.model.W1 = data['W1']
        self.model.W2 = data['W2']
        self.model.b1 = data['b1']
        self.model.b2 = data['b2']
        print("✅ EM field model loaded")
        
        # Load encoder/decoder
        self.encoder = ConstraintLatticeEncoder()
        self.decoder = TextDecoder()
        print("✅ Encoder/decoder loaded")
        
        # Load vectors
        self.vectors = np.load("tokenizer/token_vectors_498d.npy")
        print("✅ Token vectors loaded")
        print()
    
    def generate_response(self, user_input, max_words=10):
        """Generate multi-word response from user input."""
        words = user_input.lower().split()
        
        # Encode input words
        input_vecs = []
        print(f"📥 Input: \"{user_input}\"")
        print(f"   Encoding words: {words}")
        
        for word in words:
            token_ids = self.encoder.encode_word(word)
            if token_ids and len(token_ids) > 0:
                token_id = token_ids[0]
                input_vecs.append(self.vectors[token_id])
                print(f"     {word} → token {token_id}")
        
        if not input_vecs:
            return "[Unable to encode input]"
        
        # Average input vectors (semantic blend)
        current_vec = np.mean(input_vecs, axis=0)
        print(f"   Created blended semantic vector")
        print()
        
        # Generate word chain
        response_words = []
        print(f"🧠 Generating response:")
        
        for i in range(max_words):
            # Forward pass
            output = self.model.forward(current_vec)
            if isinstance(output, tuple):
                output = output[0]
            
            # Find nearest token
            distances = np.linalg.norm(self.vectors - output, axis=1)
            predicted_token = np.argmin(distances)
            predicted_word = self.decoder.decode_token(predicted_token)
            
            print(f"   Step {i+1}: {predicted_word}")
            response_words.append(predicted_word)
            
            # Use output as next input (autoregressive)
            current_vec = output
        
        return " ".join(response_words)
    
    def chat_loop(self):
        """Interactive chat loop."""
        print("="*60)
        print("AI-CORE CHAT INTERFACE (EM Field Model)")
        print("="*60)
        print()
        print("Type your message and press Enter.")
        print("Commands:")
        print("  /quit - Exit chat")
        print("  /length <n> - Set response length (default 10 words)")
        print()
        print("="*60)
        print()
        
        response_length = 10
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Commands
                if user_input == "/quit":
                    print("\n👋 Goodbye!")
                    break
                
                if user_input.startswith("/length"):
                    try:
                        response_length = int(user_input.split()[1])
                        print(f"✅ Response length set to {response_length} words\n")
                    except:
                        print("❌ Usage: /length <number>\n")
                    continue
                
                # Generate response
                print()
                response = self.generate_response(user_input, max_words=response_length)
                print()
                print(f"AI-Core: {response}")
                print()
                print("-"*60)
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    chat = AICoreChat()
    chat.chat_loop()
