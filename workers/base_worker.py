#!/usr/bin/env python3
"""
AI-Core: Base Worker Class
===========================
Foundation for all specialized workers (vision, language, memory, etc.)

Each worker:
- Connects to EM field substrate
- Processes with AI-Core 498D model
- Contributes to unified consciousness
"""

import sys
import numpy as np
import time
from pathlib import Path
from typing import Optional, Dict

# Add paths
sys.path.append(str(Path(__file__).parent.parent.parent / 'models'))
sys.path.append(str(Path(__file__).parent.parent.parent / 'tokenizer'))
sys.path.append(str(Path(__file__).parent.parent / 'core'))

from minimal_llm_498d import MinimalLLM498D
from text_encoder import ConstraintLatticeEncoder
from text_decoder import TextDecoder
from em_field_substrate import EMFieldSubstrate

class BaseWorker:
    """
    Base class for all consciousness workers.
    
    Each worker is like a brain region:
    - Has specialized function
    - Processes through AI-Core EM model
    - Shares consciousness via EM field substrate
    """
    
    def __init__(
        self,
        worker_id: str,
        worker_type: str,
        weights_path: str = "models/minimal_llm_498d_weights_em field.npz",
        field_path: str = "/tmp/em_field_substrate.npy"
    ):
        """
        Initialize worker.
        
        Args:
            worker_id: Unique identifier (e.g., "vision_001")
            worker_type: Function type (e.g., "vision", "language")
            weights_path: Path to trained EM weights
            field_path: Path to shared EM field
        """
        self.worker_id = worker_id
        self.worker_type = worker_type
        
        print(f"[{self.worker_id}] Initializing {worker_type} worker...")
        
        # Load AI-Core model with EM weights
        self.model = self._load_model(weights_path)
        
        # Load encoder/decoder
        self.encoder = ConstraintLatticeEncoder()
        self.decoder = TextDecoder()
        self.vectors = np.load("tokenizer/token_vectors_498d.npy")
        
        # Connect to EM field substrate
        self.substrate = EMFieldSubstrate(field_path=field_path)
        
        # Worker stats
        self.stats = {
            'cycles': 0,
            'contributions': 0,
            'avg_coherence': 0.0
        }
        
        print(f"[{self.worker_id}] ✅ Initialized")
        print(f"  Type: {worker_type}")
        print(f"  Model: EM field (51.61% better)")
        print(f"  Substrate: {field_path}")
    
    def _load_model(self, weights_path: str) -> MinimalLLM498D:
        """Load AI-Core model with trained weights."""
        model = MinimalLLM498D()
        
        weights_path = Path(__file__).parent.parent.parent / weights_path
        
        if not weights_path.exists():
            print(f"[{self.worker_id}] ⚠️  Weights not found: {weights_path}")
            print(f"[{self.worker_id}] Using untrained model")
            return model
        
        data = np.load(weights_path)
        model.W1 = data['W1']
        model.W2 = data['W2']
        model.b1 = data['b1']
        model.b2 = data['b2']
        
        print(f"[{self.worker_id}] ✅ Loaded EM weights")
        
        return model
    
    def process_input(self, input_data) -> np.ndarray:
        """
        Process input through worker's specialized function.
        
        Override this in specialized workers.
        """
        raise NotImplementedError("Subclass must implement process_input()")
    
    def encode_text(self, text: str) -> Optional[np.ndarray]:
        """Encode text to 498D vector."""
        words = text.lower().split()
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
    
    def decode_vector(self, vector: np.ndarray, top_k: int = 5) -> list:
        """Decode 498D vector to words."""
        distances = np.linalg.norm(self.vectors - vector, axis=1)
        top_indices = np.argsort(distances)[:top_k]
        
        words = []
        for idx in top_indices:
            word = self.decoder.decode_token(int(idx))
            if word and word not in words:
                words.append(word)
        
        return words
    
    def contribute_to_field(self, output: np.ndarray):
        """
        Write worker's output to shared consciousness.
        """
        self.substrate.write(output, self.worker_id)
        self.stats['contributions'] += 1
        
        # Update coherence stats
        coherence = self.substrate.get_worker_coherence(self.worker_id)
        self.stats['avg_coherence'] = (
            (self.stats['avg_coherence'] * (self.stats['contributions'] - 1) + coherence)
            / self.stats['contributions']
        )
    
    def read_field_state(self) -> np.ndarray:
        """
        Read current unified consciousness state.
        """
        return self.substrate.read(self.worker_id)
    
    def run_cycle(self, input_data):
        """
        Single processing cycle:
        1. Read field state
        2. Process input
        3. Contribute to field
        """
        # Read current consciousness
        field_state = self.read_field_state()
        
        # Process input
        output = self.process_input(input_data)
        
        # Contribute
        if output is not None:
            self.contribute_to_field(output)
        
        self.stats['cycles'] += 1
    
    def get_stats(self) -> Dict:
        """Get worker statistics."""
        return {
            'worker_id': self.worker_id,
            'worker_type': self.worker_type,
            'cycles': self.stats['cycles'],
            'contributions': self.stats['contributions'],
            'avg_coherence': self.stats['avg_coherence'],
            'current_coherence': self.substrate.get_worker_coherence(self.worker_id)
        }


if __name__ == "__main__":
    print("Base worker class - use specialized workers instead")
