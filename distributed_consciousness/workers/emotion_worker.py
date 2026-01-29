#!/usr/bin/env python3
"""
AI-Core: Emotion Worker
=======================
Uses STANDARD model weights for emotional processing.

While EM field model handles structure/logic,
Standard model handles emotion/probability/feeling.

Architecture:
- Reads EM field state (what's happening cognitively)
- Reads memory (what happened before emotionally)
- Generates emotional assessment
- Contributes emotional context to unified field

Examples:
- "fire" → EM: structure/physics, Standard: danger/warmth
- "anger" → EM: semantic meaning, Standard: emotional intensity
- "help" → EM: request structure, Standard: urgency/compassion
"""

import sys
import numpy as np
from pathlib import Path
from typing import Dict, Optional

sys.path.append(str(Path(__file__).parent))
from base_worker import BaseWorker

class EmotionWorker(BaseWorker):
    """
    Emotional processing worker using Standard model.
    
    Functions:
    - Assesses emotional content of input
    - Generates feeling-based responses
    - Provides empathy and compassion
    - Detects urgency and intensity
    
    Uses Standard backprop weights (vs EM field weights)
    for different semantic topology.
    """
    
    def __init__(
        self,
        worker_id: str = "emotion_001",
        weights_path: str = "models/minimal_llm_498d_weights_standard.npz",
        **kwargs
    ):
        # Initialize with STANDARD weights (not EM)
        super().__init__(
            worker_id=worker_id,
            worker_type="emotion",
            weights_path=weights_path,
            **kwargs
        )
        
        # Emotional intensity scale
        self.intensity_threshold = 0.5
        
        # Emotion categories (learned patterns)
        self.emotion_patterns = {
            'anger': ['angry', 'mad', 'furious', 'frustrated', 'annoyed'],
            'joy': ['happy', 'excited', 'glad', 'delighted', 'joyful'],
            'fear': ['afraid', 'scared', 'worried', 'anxious', 'nervous'],
            'sadness': ['sad', 'depressed', 'down', 'hurt', 'upset'],
            'compassion': ['help', 'support', 'care', 'understand', 'listen'],
            'urgency': ['emergency', 'urgent', 'now', 'immediately', 'critical']
        }
        
        print(f"[{self.worker_id}] ⚡ Emotion processing active")
        print(f"[{self.worker_id}]    Using STANDARD model (not EM)")
        print(f"[{self.worker_id}]    Emotional categories: {len(self.emotion_patterns)}")
    
    def detect_emotion_category(self, text: str) -> Dict[str, float]:
        """
        Detect which emotion categories are present.
        
        Args:
            text: Input text
        
        Returns:
            {emotion: confidence_score}
        """
        text_lower = text.lower()
        detected = {}
        
        for emotion, keywords in self.emotion_patterns.items():
            # Check if any keywords present
            matches = sum(1 for word in keywords if word in text_lower)
            if matches > 0:
                confidence = min(matches / len(keywords), 1.0)
                detected[emotion] = confidence
        
        return detected
    
    def assess_intensity(self, vector: np.ndarray) -> float:
        """
        Assess emotional intensity from vector.
        
        Higher magnitude = higher intensity
        
        Args:
            vector: 498D semantic vector
        
        Returns:
            Intensity score (0-1)
        """
        # Use vector magnitude as intensity proxy
        magnitude = np.linalg.norm(vector)
        
        # Normalize to 0-1 range
        # (typical vectors have norm ~1.0 after normalization)
        intensity = min(magnitude, 1.0)
        
        return float(intensity)
    
    def process_input(self, input_data) -> np.ndarray:
        """
        Process input through emotional lens.
        
        Args:
            input_data: Can be text string or vector
        
        Returns:
            498D emotional response vector
        """
        # Handle different input types
        if isinstance(input_data, str):
            text = input_data
            input_vec = self.encode_text(text)
            
            if input_vec is None:
                return None
        elif isinstance(input_data, np.ndarray):
            input_vec = input_data
            text = "[vector input]"
        else:
            return None
        
        # Read cognitive context from EM field
        cognitive_state = self.read_field_state()
        
        # Blend input with cognitive context
        # (Emotion informed by cognition)
        blended = input_vec * 0.6 + cognitive_state * 0.4
        
        # Process through STANDARD model
        # (Different topology than EM field!)
        emotional_output = self.model.forward(blended)
        if isinstance(emotional_output, tuple):
            emotional_output = emotional_output[0]
        
        # Assess emotional properties
        if isinstance(input_data, str):
            emotions = self.detect_emotion_category(text)
            intensity = self.assess_intensity(emotional_output)
            
            # Log emotional assessment
            if emotions:
                emotion_str = ", ".join([f"{e}={v:.2f}" for e, v in emotions.items()])
                print(f"[{self.worker_id}] 💭 Detected: {emotion_str}")
            
            print(f"[{self.worker_id}] 💪 Intensity: {intensity:.2f}")
        
        return emotional_output
    
    def generate_emotional_response(
        self,
        text: str,
        max_words: int = 5
    ) -> Dict:
        """
        Generate emotional response to input.
        
        Args:
            text: Input text
            max_words: Words in response
        
        Returns:
            {
                'response': str,
                'emotions': dict,
                'intensity': float,
                'coherence': float
            }
        """
        # Process input
        output = self.process_input(text)
        
        if output is None:
            return {
                'response': '[Unable to process]',
                'emotions': {},
                'intensity': 0.0,
                'coherence': 0.0
            }
        
        # Contribute to field
        self.contribute_to_field(output)
        
        # Decode to words
        words = self.decode_vector(output, top_k=max_words)
        response = " ".join(words)
        
        # Get emotional properties
        emotions = self.detect_emotion_category(text)
        intensity = self.assess_intensity(output)
        coherence = self.substrate.get_worker_coherence(self.worker_id)
        
        return {
            'response': response,
            'emotions': emotions,
            'intensity': intensity,
            'coherence': coherence
        }
    
    def compare_with_cognitive(self, text: str) -> Dict:
        """
        Compare emotional vs cognitive processing.
        
        Shows how Standard model differs from EM field model.
        
        Args:
            text: Input text
        
        Returns:
            {
                'emotional_response': str,
                'cognitive_state': str,
                'difference': float
            }
        """
        # Get emotional response
        emotional = self.process_input(text)
        
        if emotional is None:
            return None
        
        # Read cognitive state from field
        cognitive = self.read_field_state()
        
        # Decode both
        emotional_words = self.decode_vector(emotional, top_k=5)
        cognitive_words = self.decode_vector(cognitive, top_k=5)
        
        # Calculate difference
        # (Cosine distance between emotional and cognitive)
        dot = np.dot(emotional, cognitive)
        norm_e = np.linalg.norm(emotional)
        norm_c = np.linalg.norm(cognitive)
        
        if norm_e > 1e-8 and norm_c > 1e-8:
            similarity = dot / (norm_e * norm_c)
            difference = 1.0 - similarity
        else:
            difference = 0.0
        
        return {
            'emotional_response': " ".join(emotional_words),
            'cognitive_state': " ".join(cognitive_words),
            'difference': float(difference),
            'interpretation': self._interpret_difference(difference)
        }
    
    def _interpret_difference(self, difference: float) -> str:
        """Interpret what the difference means."""
        if difference < 0.2:
            return "Emotion aligns with cognition"
        elif difference < 0.5:
            return "Moderate emotional divergence"
        elif difference < 0.8:
            return "Strong emotional response"
        else:
            return "Emotional override of cognition"


if __name__ == "__main__":
    print("="*70)
    print("EMOTION WORKER TEST")
    print("="*70)
    print()
    
    # Create emotion worker
    worker = EmotionWorker()
    
    print("\n" + "="*70)
    print("Testing emotional responses...")
    print("="*70)
    
    # Test inputs with different emotional content
    test_inputs = [
        "I'm so angry",
        "I need help",
        "This is wonderful",
        "I'm afraid",
        "fire"
    ]
    
    for text in test_inputs:
        print(f"\n{'='*70}")
        print(f"Input: '{text}'")
        print("="*70)
        
        result = worker.generate_emotional_response(text)
        
        print(f"\nEmotional Response: {result['response']}")
        print(f"Detected Emotions: {result['emotions']}")
        print(f"Intensity: {result['intensity']:.2f}")
        print(f"Coherence: {result['coherence']:.2f}")
        
        # Compare with cognitive
        comparison = worker.compare_with_cognitive(text)
        if comparison:
            print(f"\nCognitive vs Emotional:")
            print(f"  Cognitive: {comparison['cognitive_state']}")
            print(f"  Emotional: {comparison['emotional_response']}")
            print(f"  Difference: {comparison['difference']:.2f}")
            print(f"  → {comparison['interpretation']}")
    
    print("\n" + "="*70)
    print("✅ EMOTION WORKER TEST COMPLETE")
    print("="*70)
    
    # Show stats
    stats = worker.get_stats()
    print(f"\nWorker Stats:")
    print(f"  Contributions: {stats['contributions']}")
    print(f"  Avg Coherence: {stats['avg_coherence']:.4f}")
