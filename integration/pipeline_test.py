#!/usr/bin/env python3
"""
AI-Core Standalone: Full Pipeline Integration Test
===================================================

Tests the complete text→inference→text pipeline:
  1. Text Encoder (words → tokens)
  2. MinimalLLM (inference on 82D vectors)
  3. Text Decoder (tokens → words)

This proves the standalone system works end-to-end.

Author: comanderanch
Phase: 5.7 Standalone Resurrection
"""

import sys
import numpy as np
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tokenizer.text_encoder import ConstraintLatticeEncoder
from tokenizer.text_decoder import TextDecoder


class MinimalLLMWrapper:
    """
    Wrapper for MinimalLLM to integrate with encoder/decoder.
    
    Handles:
      - Loading trained weights
      - Token indices → 82D vectors
      - Forward pass inference
      - Output → nearest token
    """
    
    def __init__(
        self,
        weights_path: str = "memory/model_weights.npz",
        token_influence_path: str = "tokenizer/token_influence_vectors.npy"
    ):
        """
        Initialize MinimalLLM with trained weights.
        
        Args:
            weights_path: Path to model_weights.npz
            token_influence_path: Path to 82D token vectors
        """
        self.weights_path = Path(weights_path)
        self.token_influence_path = Path(token_influence_path)
        
        # Load model weights
        self.W1, self.W2 = self._load_weights()
        
        # Load token influence vectors (82D representations)
        self.token_vectors = self._load_token_vectors()
        
        print(f"[✓] MinimalLLM loaded")
        print(f"    Weights: {self.W1.shape} → {self.W2.shape}")
        print(f"    Token vectors: {self.token_vectors.shape}")
    
    def _load_weights(self):
        """Load trained model weights."""
        if not self.weights_path.exists():
            print(f"[!] Warning: No trained weights at {self.weights_path}")
            print(f"    Using random initialization")
            W1 = np.random.randn(82, 8) * 0.1
            W2 = np.random.randn(8, 82) * 0.1
            return W1, W2
        
        data = np.load(self.weights_path)
        W1 = data['W1']
        W2 = data['W2']
        return W1, W2
    
    def _load_token_vectors(self):
        """Load 82D token influence vectors."""
        if not self.token_influence_path.exists():
            print(f"[!] Warning: No token vectors at {self.token_influence_path}")
            print(f"    Using zero vectors")
            return np.zeros((2304, 82))
        
        vectors = np.load(self.token_influence_path)
        return vectors
    
    def token_to_vector(self, token_id: int) -> np.ndarray:
        """
        Convert token ID to 82D vector.
        
        Args:
            token_id: Token index (0-2303)
        
        Returns:
            82D numpy array
        """
        if 0 <= token_id < len(self.token_vectors):
            return self.token_vectors[token_id]
        else:
            # Out of range - return zero vector
            return np.zeros(82)
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        MinimalLLM forward pass.
        
        Architecture: 82 → 8 → 82 (bottleneck)
        
        Args:
            x: Input vector (82D)
        
        Returns:
            Output vector (82D)
        """
        # Layer 1: 82 → 8
        hidden = np.tanh(x @ self.W1)
        
        # Layer 2: 8 → 82
        output = hidden @ self.W2
        
        return output
    
    def predict_next_token(self, token_id: int) -> int:
        """
        Predict next token given current token.
        
        Args:
            token_id: Current token ID
        
        Returns:
            Predicted next token ID
        """
        # Get 82D vector for token
        x = self.token_to_vector(token_id)
        
        # Forward pass
        output = self.forward(x)
        
        # Find nearest token vector to output
        nearest_id = self._find_nearest_token(output)
        
        return nearest_id
    
    def _find_nearest_token(self, vector: np.ndarray) -> int:
        """
        Find token with nearest vector to output.
        
        Uses cosine similarity.
        
        Args:
            vector: 82D output vector
        
        Returns:
            Token ID with highest similarity
        """
        # Normalize vector
        vec_norm = vector / (np.linalg.norm(vector) + 1e-8)
        
        # Compute similarities with all token vectors
        token_norms = self.token_vectors / (
            np.linalg.norm(self.token_vectors, axis=1, keepdims=True) + 1e-8
        )
        similarities = token_norms @ vec_norm
        
        # Return token with highest similarity
        best_id = np.argmax(similarities)
        return int(best_id)


class StandalonePipeline:
    """
    Complete standalone inference pipeline.
    
    Text → Tokens → Inference → Tokens → Text
    """
    
    def __init__(self):
        """Initialize all components."""
        print("="*60)
        print("INITIALIZING STANDALONE PIPELINE")
        print("="*60)
        
        # Load encoder
        self.encoder = ConstraintLatticeEncoder(
            word_map_path="tokenizer/word_token_map.json",
            color_tokens_path="tokenizer/full_color_tokens.csv",
            learning_mode=True
        )
        
        # Load decoder
        self.decoder = TextDecoder(
            word_map_path="tokenizer/word_token_map.json"
        )
        
        # Load MinimalLLM
        self.llm = MinimalLLMWrapper(
            weights_path="memory/model_weights.npz",
            token_influence_path="tokenizer/token_influence_vectors.npy"
        )
        
        print("="*60)
        print("[✓] Pipeline ready")
        print("="*60)
    
    def infer(self, text: str, steps: int = 1) -> str:
        """
        Run full inference pipeline.
        
        Args:
            text: Input text
            steps: Number of prediction steps
        
        Returns:
            Generated text
        """
        print(f"\n[INPUT] '{text}'")
        
        # Step 1: Encode text to tokens
        token_ids = self.encoder.encode_sentence(text)
        print(f"[ENCODE] Tokens: {token_ids[:10]}..." if len(token_ids) > 10 else f"[ENCODE] Tokens: {token_ids}")
        
        if not token_ids:
            return "[ERROR: No tokens generated]"
        
        # Step 2: Run inference for N steps
        current_token = token_ids[-1]  # Start from last token
        predicted_tokens = []
        
        for step in range(steps):
            next_token = self.llm.predict_next_token(current_token)
            predicted_tokens.append(next_token)
            current_token = next_token
            print(f"[STEP {step+1}] Predicted token: {next_token}")
        
        # Step 3: Decode predicted tokens to text
        output_text = self.decoder.decode_tokens(predicted_tokens)
        print(f"[DECODE] '{output_text}'")
        
        return output_text
    
    def interactive_mode(self):
        """Interactive testing mode."""
        print("\n" + "="*60)
        print("INTERACTIVE MODE")
        print("Type 'quit' to exit")
        print("="*60)
        
        while True:
            try:
                user_input = input("\nYOU> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Exiting...")
                    break
                
                if not user_input:
                    continue
                
                # Run inference
                output = self.infer(user_input, steps=3)
                print(f"AI> {output}")
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break


# Test suite
if __name__ == "__main__":
    print("\n" + "="*60)
    print("STANDALONE PIPELINE - INTEGRATION TEST")
    print("="*60)
    
    # Initialize pipeline
    pipeline = StandalonePipeline()
    
    # Test 1: Simple inference
    print("\n" + "="*60)
    print("[TEST 1] Single word inference")
    print("="*60)
    result = pipeline.infer("fire", steps=1)
    print(f"Result: '{result}'")
    
    # Test 2: Multi-word input
    print("\n" + "="*60)
    print("[TEST 2] Multi-word inference")
    print("="*60)
    result = pipeline.infer("the sky", steps=2)
    print(f"Result: '{result}'")
    
    # Test 3: Known semantic pair
    print("\n" + "="*60)
    print("[TEST 3] Semantic association (if trained)")
    print("="*60)
    result = pipeline.infer("hot", steps=1)
    print(f"Result: '{result}' (expect: related to fire/heat)")
    
    # Test 4: Interactive mode (optional)
    print("\n" + "="*60)
    print("Ready for interactive testing?")
    print("="*60)
    
    response = input("Start interactive mode? (y/n): ").strip().lower()
    if response == 'y':
        pipeline.interactive_mode()
    else:
        print("\nTest complete. Pipeline ready for use.")