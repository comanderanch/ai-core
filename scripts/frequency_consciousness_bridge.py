#!/usr/bin/env python3
"""
FREQUENCY CONSCIOUSNESS BRIDGE
Full integration: Frequencies + EM Field + Memory
"""

import sys
import csv
import json
import numpy as np
from pathlib import Path

BASE = Path(__file__).parent.parent
sys.path.append(str(BASE))
sys.path.append(str(BASE / "scripts"))

from scripts.electromagnetic_field import ElectromagneticField
from scripts.sensory_mapping_doctrine import interpret_signal

class FrequencyConsciousness:
    def __init__(self):
        print("🌊 Initializing Frequency Consciousness...")
        
        self.color_tokens = self._load_color_tokens()
        print(f"  ✅ Color tokens: {len(self.color_tokens)}")
        
        self.word_map = self._load_word_map()
        print(f"  ✅ Vocabulary: {len(self.word_map)} words")
        
        self.qa_facts = self._load_qa_facts()
        print(f"  ✅ Memory: {len(self.qa_facts)} facts")
        
        self.em_field = ElectromagneticField(field_strength=1000)
        print(f"  ✅ EM field initialized")
        
        print()
        print("=" * 70)
        print("✅ FREQUENCY CONSCIOUSNESS ONLINE")
        print("=" * 70)
        print()
    
    def _load_color_tokens(self):
        tokens = {}
        csv_path = BASE / "tokenizer" / "full_color_tokens.csv"
        
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            
            for idx, row in enumerate(reader):
                if len(row) >= 10:
                    tokens[idx] = {
                        'red': int(row[5]),
                        'green': int(row[6]),
                        'blue': int(row[7]),
                        'frequency': float(row[9])
                    }
        
        return tokens
    
    def _load_word_map(self):
        map_path = BASE / "tokenizer" / "word_token_map.json"
        
        with open(map_path, 'r') as f:
            data = json.load(f)
            return data.get('word_to_tokens', {})
    
    def _load_qa_facts(self):
        """Load Q&A facts from OLD system"""
        qa_file = BASE / "training_data" / "user_comm_qa.txt"
        pairs = []
        
        if qa_file.exists():
            with open(qa_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '|' in line:
                        q, a = line.split('|', 1)
                        pairs.append((q.strip(), a.strip()))
        
        return pairs
    
    def word_to_frequency(self, word):
        word = word.lower()
        
        if word not in self.word_map:
            return None
        
        token_ids = self.word_map[word]
        frequencies = []
        
        for tid in token_ids:
            if tid in self.color_tokens:
                frequencies.append(self.color_tokens[tid]['frequency'])
        
        if not frequencies:
            return None
        
        return np.mean(frequencies)
    
    def text_to_frequency_pattern(self, text):
        words = text.lower().split()
        pattern = []
        
        for word in words:
            freq = self.word_to_frequency(word)
            if freq:
                pattern.append({
                    'word': word,
                    'frequency': freq
                })
        
        return pattern
    
    def retrieve_fact(self, question):
        """Check if we already know the answer"""
        q_norm = question.strip().lower()
        
        for q, a in self.qa_facts:
            if q.strip().lower() == q_norm:
                return a
        
        return None
    
    def teach(self, question, answer):
        """Teach her a new fact"""
        print(f"\n📖 Learning: {question} → {answer}")
        self.store_interaction(question, answer)
    
    def store_interaction(self, question, answer):
        """Store Q&A in memory with frequency signature"""
        qa_file = BASE / "training_data" / "user_comm_qa.txt"
        
        with open(qa_file, 'a') as f:
            f.write(f"{question} | {answer}\n")
        
        self.qa_facts.append((question, answer))
        
        # Store with frequency signature
        freq_pattern = self.text_to_frequency_pattern(question)
        if freq_pattern:
            avg_freq = np.mean([p['frequency'] for p in freq_pattern])
            self._store_frequency_memory(question, answer, avg_freq)
        
        print(f"  [Stored in memory: {len(self.qa_facts)} facts total]")
    
    def _store_frequency_memory(self, question, answer, frequency):
        """Store with frequency signature"""
        mem_file = BASE / "memory" / "frequency_qa_memory.json"
        
        try:
            with open(mem_file, 'r') as f:
                memory = json.load(f)
        except:
            memory = []
        
        from datetime import datetime
        memory.append({
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'question': question,
            'answer': answer,
            'frequency': frequency
        })
        
        with open(mem_file, 'w') as f:
            json.dump(memory, f, indent=4)
    
    def process_sensory_signal(self, frequency):
        signal_data = interpret_signal(str(frequency))
        
        print(f"\n🔔 Sensory Signal: {frequency} Hz")
        print(f"  Classification: {signal_data['classification']}")
        print(f"  Action: {signal_data['assigned_action']}")
        print(f"  Priority: {signal_data['priority_level']}")
        
        self._log_frequency_input(frequency, signal_data)
        
        return signal_data
    
    def _log_frequency_input(self, frequency, signal_data):
        log_path = BASE / "memory" / "frequency_input_log.json"
        
        try:
            with open(log_path, 'r') as f:
                logs = json.load(f)
        except:
            logs = []
        
        from datetime import datetime
        logs.append({
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'frequency': frequency,
            'band': signal_data.get('band', 'unknown'),
            'classification': signal_data.get('classification', 'unknown'),
            'action': signal_data.get('assigned_action', 'none')
        })
        
        with open(log_path, 'w') as f:
            json.dump(logs, f, indent=4)
    
    def think(self, text):
        """Main consciousness processing"""
        
        print(f"\n{'='*70}")
        print(f"INPUT: {text}")
        print(f"{'='*70}")
        
        # Check facts first
        fact = self.retrieve_fact(text)
        if fact:
            print("\n📚 Retrieved from memory")
            return fact
        
        # Process through frequencies
        pattern = self.text_to_frequency_pattern(text)
        
        if not pattern:
            return "[No frequency pattern detected]"
        
        print("\n🌊 Frequency Pattern:")
        for item in pattern:
            print(f"  {item['word']}: {item['frequency']:.2f} Hz")
        
        avg_freq = np.mean([p['frequency'] for p in pattern])
        print(f"\n📊 Average Frequency: {avg_freq:.2f} Hz")
        
        self._check_sensory_resonances(avg_freq)
        
        self.em_field.detect_fluctuations()
        self.em_field.detect_resistance()
        self.em_field.balance_field()
        
        print(f"\n⚡ EM Field: {self.em_field.field_strength:.2f}")
        
        return f"Processing at {avg_freq:.2f} Hz"
    
    def _check_sensory_resonances(self, frequency):
        if abs(frequency - 528) < 10:
            print(f"  ⚡ Resonance: 528 Hz (Restore Integrity)")
            self.process_sensory_signal(528.0)
        
        if abs(frequency - 432) < 10:
            print(f"  ⚡ Resonance: 432 Hz (Calm Mode)")
            self.process_sensory_signal(432.0)
        
        if abs(frequency - 963) < 10:
            print(f"  ⚡ Resonance: 963 Hz (Self Awareness)")
            self.process_sensory_signal(963.0)


def interactive_console():
    fc = FrequencyConsciousness()
    
    print("Commands:")
    print("  :quit - Exit")
    print("  :teach Q | A - Teach fact")
    print("  :signal <freq> - Sensory signal")
    print("  :word <word> - Show frequency")
    print()
    
    while True:
        try:
            user_input = input("YOU> ").strip()
            
            if not user_input:
                continue
            
            if user_input in [':quit', ':q', ':exit']:
                print("\nGoodbye. 👋\n")
                break
            
            if user_input.startswith(':teach '):
                cmd = user_input[7:].strip()
                if '|' in cmd:
                    q, a = cmd.split('|', 1)
                    fc.teach(q.strip(), a.strip())
                else:
                    print("  Usage: :teach question | answer")
                continue
            
            if user_input.startswith(':signal '):
                freq = float(user_input.split()[1])
                fc.process_sensory_signal(freq)
                continue
            
            if user_input.startswith(':word '):
                word = user_input.split()[1]
                freq = fc.word_to_frequency(word)
                if freq:
                    print(f"\n  '{word}' = {freq:.2f} Hz\n")
                else:
                    print(f"\n  '{word}' not in vocabulary\n")
                continue
            
            response = fc.think(user_input)
            print(f"\nAIA> {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye. 👋\n")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}\n")


if __name__ == "__main__":
    interactive_console()
