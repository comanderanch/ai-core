#!/usr/bin/env python3
"""
AI-Core: Memory Worker
======================
Stores experiences, recalls context, maintains history.

Like hippocampus in the brain.
"""

import sys
import numpy as np
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

sys.path.append(str(Path(__file__).parent))
from base_worker import BaseWorker

class MemoryWorker(BaseWorker):
    """
    Specialized worker for memory storage/retrieval.
    
    Functions:
    - Stores semantic vectors (experiences)
    - Retrieves similar memories
    - Maintains conversation history
    - Provides context to other workers
    """
    
    def __init__(
        self, 
        worker_id: str = "memory_001",
        memory_path: str = "/tmp/aicore_memories.json",
        **kwargs
    ):
        super().__init__(
            worker_id=worker_id,
            worker_type="memory",
            **kwargs
        )
        
        self.memory_path = Path(memory_path)
        self.memories = self._load_memories()
        
        print(f"[{self.worker_id}] Loaded {len(self.memories)} memories")
    
    def _load_memories(self) -> List[Dict]:
        """Load existing memories from disk."""
        if self.memory_path.exists():
            with open(self.memory_path, 'r') as f:
                return json.load(f)
        return []
    
    def _save_memories(self):
        """Save memories to disk."""
        with open(self.memory_path, 'w') as f:
            json.dump(self.memories, f, indent=2)
    
    def process_input(self, data: Dict) -> np.ndarray:
        """
        Process and store memory.
        
        Args:
            data: {
                'vector': np.ndarray (498D),
                'text': str (optional),
                'metadata': dict (optional)
            }
        
        Returns:
            Retrieved context vector
        """
        input_vec = data.get('vector')
        
        if input_vec is None:
            return None
        
        # Store memory
        memory = {
            'timestamp': datetime.now().isoformat(),
            'vector': input_vec.tolist(),
            'text': data.get('text', ''),
            'metadata': data.get('metadata', {})
        }
        
        self.memories.append(memory)
        
        # Keep last 1000 memories
        if len(self.memories) > 1000:
            self.memories = self.memories[-1000:]
        
        self._save_memories()
        
        # Retrieve similar memories (context)
        context = self.recall_similar(input_vec, top_k=3)
        
        if context:
            # Average context vectors
            context_vecs = [np.array(m['vector']) for m in context]
            context_vec = np.mean(context_vecs, axis=0)
            return context_vec
        
        return input_vec
    
    def recall_similar(self, query_vec: np.ndarray, top_k: int = 5) -> List[Dict]:
        """
        Recall memories similar to query.
        
        Args:
            query_vec: Query vector (498D)
            top_k: Number of memories to return
        
        Returns:
            List of similar memories
        """
        if not self.memories:
            return []
        
        # Calculate similarities
        similarities = []
        
        for memory in self.memories:
            mem_vec = np.array(memory['vector'])
            
            # Cosine similarity
            dot = np.dot(query_vec, mem_vec)
            norm_q = np.linalg.norm(query_vec)
            norm_m = np.linalg.norm(mem_vec)
            
            if norm_q > 1e-8 and norm_m > 1e-8:
                similarity = dot / (norm_q * norm_m)
                similarities.append((similarity, memory))
        
        # Sort by similarity
        similarities.sort(reverse=True, key=lambda x: x[0])
        
        # Return top k
        return [mem for _, mem in similarities[:top_k]]
    
    def get_recent_context(self, n: int = 5) -> np.ndarray:
        """Get average of recent memories."""
        if not self.memories:
            return np.zeros(498)
        
        recent = self.memories[-n:]
        vectors = [np.array(m['vector']) for m in recent]
        
        return np.mean(vectors, axis=0)


if __name__ == "__main__":
    print("="*60)
    print("MEMORY WORKER TEST")
    print("="*60)
    
    # Create worker
    worker = MemoryWorker()
    
    # Store some memories
    print("\nStoring memories...")
    
    test_memories = [
        {'text': 'fire is hot', 'vector': np.random.randn(498)},
        {'text': 'water is cold', 'vector': np.random.randn(498)},
        {'text': 'sky is blue', 'vector': np.random.randn(498)}
    ]
    
    for mem in test_memories:
        worker.process_input(mem)
        print(f"  Stored: {mem['text']}")
    
    # Recall
    print("\nRecalling similar to 'fire'...")
    query = np.random.randn(498)
    similar = worker.recall_similar(query, top_k=2)
    
    for mem in similar:
        print(f"  Recalled: {mem['text']}")
    
    print(f"\n✅ Memory worker has {len(worker.memories)} memories")
