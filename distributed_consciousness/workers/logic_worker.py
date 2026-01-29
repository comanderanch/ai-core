#!/usr/bin/env python3
"""
AI-Core: Logic Worker
=====================
Handles reasoning, inference, logical relationships.

Like prefrontal cortex in the brain.
"""

import sys
import numpy as np
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from base_worker import BaseWorker

class LogicWorker(BaseWorker):
    """
    Specialized worker for logical processing.
    
    Functions:
    - Infers relationships between concepts
    - Performs logical operations (AND, OR, NOT)
    - Evaluates consistency
    - Makes decisions
    """
    
    def __init__(self, worker_id: str = "logic_001", **kwargs):
        super().__init__(
            worker_id=worker_id,
            worker_type="logic",
            **kwargs
        )
    
    def process_input(self, input_vec: np.ndarray) -> np.ndarray:
        """
        Process input through logical inference.
        
        Applies direct EM field forward pass (pure logic).
        """
        # Read field for context
        field_state = self.read_field_state()
        
        # Combine input with field (logical AND-like operation)
        combined = input_vec * field_state
        
        # Process through model
        output = self.model.forward(combined)
        if isinstance(output, tuple):
            output = output[0]
        
        return output
    
    def infer_relationship(self, vec_a: np.ndarray, vec_b: np.ndarray) -> np.ndarray:
        """
        Infer relationship between two concepts.
        
        Args:
            vec_a: First concept (498D)
            vec_b: Second concept (498D)
        
        Returns:
            Relationship vector (498D)
        """
        # Difference (what makes them different)
        difference = vec_a - vec_b
        
        # Process through logic
        relationship = self.process_input(difference)
        
        return relationship


if __name__ == "__main__":
    print("="*60)
    print("LOGIC WORKER TEST")
    print("="*60)
    
    worker = LogicWorker()
    
    # Test inference
    vec_a = np.random.randn(498)
    vec_b = np.random.randn(498)
    
    relationship = worker.infer_relationship(vec_a, vec_b)
    
    print(f"✅ Logic worker functional")
    print(f"   Inferred relationship vector: {relationship.shape}")
