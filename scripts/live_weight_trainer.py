#!/usr/bin/env python3
"""
LIVE WEIGHT TRAINER
Continuously updates 498D EM field weights from new Q&A facts
"""

import sys
import json
import time
import numpy as np
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent
sys.path.append(str(BASE))

from models.minimal_llm_498d import MinimalLLM498D
from tokenizer.text_encoder import ConstraintLatticeEncoder

class LiveWeightTrainer:
    def __init__(self):
        print("🔥 Initializing Live Weight Trainer...")
        print()
        
        self.qa_file = BASE / "training_data" / "user_comm_qa.txt"
        self.em_weights_file = BASE / "models" / "minimal_llm_498d_weights_em field.npz"
        
        # Load 498D model
        self.model = MinimalLLM498D()
        self._load_weights()
        
        # Load token vectors and word map
        self.vectors = np.load(BASE / "tokenizer" / "token_vectors_498d.npy")
        
        with open(BASE / "tokenizer" / "word_token_map.json", 'r') as f:
            data = json.load(f)
            self.word_to_tokens = data['word_to_tokens']
        
        # Training params
        self.learning_rate = 0.01
        self.last_trained_line = self._get_last_trained_line()
        
        print(f"  ✅ Model loaded (498D → 64D → 498D)")
        print(f"  ✅ Last trained line: {self.last_trained_line}")
        print(f"  ✅ Learning rate: {self.learning_rate}")
        print()
    
    def _load_weights(self):
        """Load existing weights"""
        if self.em_weights_file.exists():
            data = np.load(self.em_weights_file)
            self.model.W1 = data['W1']
            self.model.W2 = data['W2']
            self.model.b1 = data['b1']
            self.model.b2 = data['b2']
            print("  ✅ Existing weights loaded")
        else:
            print("  ⚠️  No existing weights, using initialized values")
    
    def _save_weights(self):
        """Save updated weights"""
        np.savez(
            self.em_weights_file,
            W1=self.model.W1,
            W2=self.model.W2,
            b1=self.model.b1,
            b2=self.model.b2
        )
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"  💾 Weights saved: {timestamp}")
    
    def _get_last_trained_line(self):
        """Get last line number we trained on"""
        tracker_file = BASE / "memory" / "training_tracker.json"
        
        if tracker_file.exists():
            with open(tracker_file, 'r') as f:
                data = json.load(f)
                return data.get('last_line', 0)
        
        return 0
    
    def _update_training_tracker(self, line_num):
        """Update training progress"""
        tracker_file = BASE / "memory" / "training_tracker.json"
        tracker_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(tracker_file, 'w') as f:
            json.dump({
                'last_line': line_num,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }, f, indent=4)
    
    def text_to_vector(self, text):
        """Convert text to 498D vector"""
        words = text.lower().split()
        vectors = []
        
        for word in words:
            if word in self.word_to_tokens:
                token_ids = self.word_to_tokens[word]
                for tid in token_ids[:1]:  # First token only
                    if tid < len(self.vectors):
                        vectors.append(self.vectors[tid])
        
        if not vectors:
            return np.zeros(498)
        
        return np.mean(vectors, axis=0)
    
    def get_new_training_pairs(self):
        """Get new Q&A pairs since last training"""
        if not self.qa_file.exists():
            return []
        
        new_pairs = []
        
        with open(self.qa_file, 'r') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines[self.last_trained_line:], start=self.last_trained_line):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if '|' in line:
                q, a = line.split('|', 1)
                new_pairs.append((q.strip(), a.strip(), i + 1))
        
        return new_pairs
    
    def train_on_pair(self, question, answer):
        """Train model on one Q&A pair"""
        
        # Convert to vectors
        q_vec = self.text_to_vector(question)
        a_vec = self.text_to_vector(answer)
        
        # Forward pass - model returns (output, metadata)
        output, metadata = self.model.forward(q_vec)
        
        # Calculate loss
        loss = np.mean((output - a_vec) ** 2)
        
        # Backward pass (simplified gradient descent)
        output_error = output - a_vec
        
        # Get hidden layer from metadata
        hidden = metadata['a1']  # Activated hidden layer
        
        # Update W2 and b2
        self.model.W2 -= self.learning_rate * np.outer(hidden, output_error)
        self.model.b2 -= self.learning_rate * output_error
        
        # Update W1 and b1
        hidden_error = np.dot(self.model.W2, output_error)
        hidden_error = hidden_error * (hidden > 0)  # ReLU derivative
        
        self.model.W1 -= self.learning_rate * np.outer(q_vec, hidden_error)
        self.model.b1 -= self.learning_rate * hidden_error
        
        return loss
    
    def run_training_cycle(self):
        """Check for new facts and train"""
        
        new_pairs = self.get_new_training_pairs()
        
        if not new_pairs:
            return 0
        
        print(f"\n🎓 Training on {len(new_pairs)} new facts...")
        
        total_loss = 0
        
        for q, a, line_num in new_pairs:
            loss = self.train_on_pair(q, a)
            total_loss += loss
            self.last_trained_line = line_num
        
        avg_loss = total_loss / len(new_pairs)
        
        print(f"  📊 Average loss: {avg_loss:.4f}")
        print(f"  ✅ Trained through line: {self.last_trained_line}")
        
        # Save weights and progress
        self._save_weights()
        self._update_training_tracker(self.last_trained_line)
        
        return len(new_pairs)
    
    def run_daemon(self, check_interval=10):
        """Run as background daemon"""
        
        print("=" * 70)
        print("🔥 LIVE WEIGHT TRAINER DAEMON")
        print("=" * 70)
        print()
        print(f"Monitoring: {self.qa_file}")
        print(f"Check interval: {check_interval} seconds")
        print()
        print("Press Ctrl+C to stop")
        print()
        
        try:
            while True:
                trained = self.run_training_cycle()
                
                if trained > 0:
                    print(f"  ⚡ Model improved! (+{trained} facts)\n")
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping trainer...")
            self._save_weights()
            print("✅ Final weights saved")
            print("Goodbye. 👋\n")


if __name__ == "__main__":
    trainer = LiveWeightTrainer()
    trainer.run_daemon(check_interval=10)
