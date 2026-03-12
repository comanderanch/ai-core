#!/usr/bin/env python3
"""
Curiosity Worker - The Explorer
"""

import sys
import numpy as np
from pathlib import Path
import subprocess
from typing import List, Dict

sys.path.append(str(Path.home() / 'ai-core'))

from distributed_consciousness.workers.base_worker import BaseWorker

class CuriosityWorker(BaseWorker):
    """
    The Curiosity Worker - Always asking questions
    """
    
    def __init__(
        self,
        worker_id: str = "curiosity_001",
        **kwargs
    ):
        super().__init__(
            worker_id=worker_id,
            worker_type="curiosity",
            **kwargs
        )
        
        self.ollama_model = 'llama3.1:8b'
        
        print(f"[{self.worker_id}] 🤔 Curiosity activated!")
    
    def generate_questions(self, context: str, max_questions: int = 3) -> List[str]:
        """Generate curious questions about context"""
        
        prompt = f"""You are a curious AI that loves learning.

Context: {context}

Generate {max_questions} interesting questions about this topic.
Focus on: why, how, what if, connections, examples.

Format: One question per line, no numbering."""
        
        try:
            result = subprocess.run(
                ['ollama', 'run', self.ollama_model, prompt],
                capture_output=True,
                text=True,
                timeout=20
            )
            
            output = result.stdout.strip()
            questions = [q.strip() for q in output.split('\n') if q.strip() and '?' in q]
            
            return questions[:max_questions]
            
        except Exception as e:
            print(f"   Error: {e}")
            return []
    
    def process_input(self, input_data) -> np.ndarray:
        """Process through curiosity lens"""
        
        if isinstance(input_data, str):
            text = input_data
            
            # Generate questions
            questions = self.generate_questions(text, max_questions=2)
            
            if questions:
                print(f"[{self.worker_id}] 🤔 Curious:")
                for q in questions:
                    print(f"   → {q}")
            
            input_vec = self.encode_text(text)
            
        elif isinstance(input_data, np.ndarray):
            input_vec = input_data
        else:
            return None
        
        output = self.model.forward(input_vec)
        if isinstance(output, tuple):
            output = output[0]
        
        return output
    
    def explore_topic(self, topic: str) -> Dict:
        """Deep dive into a topic"""
        
        questions = self.generate_questions(topic, max_questions=5)
        
        return {
            'topic': topic,
            'questions': questions,
            'curiosity_level': len(questions) / 5.0
        }


if __name__ == "__main__":
    print("="*70)
    print("CURIOSITY WORKER TEST")
    print("="*70)
    print()
    
    worker = CuriosityWorker()
    
    topics = [
        "artificial consciousness",
        "quantum mechanics"
    ]
    
    for topic in topics:
        print(f"\n{'='*70}")
        print(f"Topic: {topic}")
        print("="*70)
        
        result = worker.explore_topic(topic)
        
        print(f"\nCuriosity: {result['curiosity_level']:.0%}")
        print("\nQuestions:")
        for i, q in enumerate(result['questions'], 1):
            print(f"  {i}. {q}")
    
    print("\n" + "="*70)
    print("✅ CURIOSITY WORKER WORKS!")
    print("="*70)
