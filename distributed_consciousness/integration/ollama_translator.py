#!/usr/bin/env python3
"""
Ollama Language Translation Layer
==================================
Translates 498D semantic understanding to natural language.

Workers understand concepts (498D vectors)
Ollama translates to human language
"""

import subprocess
import numpy as np
from typing import Dict, List

class OllamaTranslator:
    """
    Translates worker semantic output to natural language
    """
    
    def __init__(self):
        # Subject-specific teachers
        self.teachers = {
            'cognitive': 'llama3.1:8b',
            'emotion': 'llama3.1:8b',
            'psychology': 'llama3.1:8b',
            'code': 'qwen2.5-coder:14b',
            'science': 'llama3.1:8b',
            'general': 'llama3.1:8b'
        }
        
        print("🗣️  Ollama Translator initialized")
    
    def translate_worker_output(
        self,
        worker_name: str,
        worker_type: str,
        raw_output: str,
        context: str
    ) -> str:
        """
        Worker says: "ufsdump semicircular knowledge"
        Ollama translates: "Processing spatial information patterns"
        """
        
        # Choose appropriate teacher
        teacher = self.teachers.get(worker_type, 'general')
        
        prompt = f"""You are translating AI semantic output to natural language.

Context: {context}
Worker: {worker_name} ({worker_type})
Semantic output: {raw_output}

Translate this into ONE clear sentence that explains what the AI is understanding.
Be concise and natural. No preamble."""
        
        try:
            result = subprocess.run(
                ['ollama', 'run', teacher, prompt],
                capture_output=True,
                text=True,
                timeout=20
            )
            
            translation = result.stdout.strip()
            
            # Clean up
            lines = translation.split('\n')
            for line in lines:
                if line and not line.startswith('[') and len(line) > 10:
                    return line.strip()
            
            return translation
            
        except subprocess.TimeoutExpired:
            return raw_output  # Fallback to raw
        except Exception as e:
            return raw_output
    
    def synthesize_perspectives(
        self,
        context: str,
        worker_outputs: Dict[str, str]
    ) -> str:
        """
        Multiple workers have spoken
        Synthesize into unified natural response
        """
        
        prompt = f"""User asked: {context}

Different AI perspectives:
"""
        for worker, output in worker_outputs.items():
            prompt += f"\n{worker}: {output}"
        
        prompt += "\n\nSynthesize these perspectives into ONE clear, natural response. Be concise."
        
        try:
            result = subprocess.run(
                ['ollama', 'run', 'llama3.1:8b', prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return result.stdout.strip()
            
        except:
            # Fallback: just combine
            return ". ".join(worker_outputs.values())
