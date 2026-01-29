#!/usr/bin/env python3
"""
AI-Core: Language Worker
========================
Processes text, generates responses, handles conversation.

Like Broca's and Wernicke's areas in the brain.
"""

import sys
import numpy as np
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from base_worker import BaseWorker

class LanguageWorker(BaseWorker):
    """
    Specialized worker for language processing.
    
    Functions:
    - Encodes text to 498D semantic space
    - Processes through EM field model
    - Generates text responses
    - Handles conversation flow
    """
    
    def __init__(self, worker_id: str = "language_001", **kwargs):
        super().__init__(
            worker_id=worker_id,
            worker_type="language",
            **kwargs
        )
    
    def process_input(self, text: str) -> np.ndarray:
        """
        Process text input.
        
        Args:
            text: Input text/prompt
        
        Returns:
            498D semantic vector
        """
        # Encode text to vector
        input_vec = self.encode_text(text)
        
        if input_vec is None:
            print(f"[{self.worker_id}] Unable to encode: {text}")
            return None
        
        # Read current field state (context)
        field_state = self.read_field_state()
        
        # Blend input with field (context-aware processing)
        blended = input_vec * 0.7 + field_state * 0.3
        
        # Process through EM model
        output = self.model.forward(blended)
        if isinstance(output, tuple):
            output = output[0]
        
        return output
    
    def generate_response(self, prompt: str, max_words: int = 5) -> str:
        """
        Generate text response to prompt.
        
        Args:
            prompt: Input text
            max_words: Number of words to generate
        
        Returns:
            Generated text
        """
        print(f"\n[{self.worker_id}] Processing: \"{prompt}\"")
        
        # Process input
        output = self.process_input(prompt)
        
        if output is None:
            return "[Unable to process]"
        
        # Contribute to field
        self.contribute_to_field(output)
        
        # Decode to words
        words = self.decode_vector(output, top_k=max_words)
        
        response = " ".join(words)
        
        # Stats
        coherence = self.substrate.get_worker_coherence(self.worker_id)
        print(f"[{self.worker_id}] Response: \"{response}\"")
        print(f"[{self.worker_id}] Coherence: {coherence:.4f}")
        
        return response


if __name__ == "__main__":
    print("="*60)
    print("LANGUAGE WORKER TEST")
    print("="*60)
    
    # Create worker
    worker = LanguageWorker()
    
    # Test prompts
    prompts = [
        "fire",
        "red hot",
        "consciousness",
        "blue water"
    ]
    
    for prompt in prompts:
        response = worker.generate_response(prompt)
        print()
    
    # Show stats
    print("="*60)
    print("WORKER STATS:")
    stats = worker.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ LANGUAGE WORKER TEST COMPLETE")
