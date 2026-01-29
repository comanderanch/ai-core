#!/usr/bin/env python3
"""
Self-Teaching Consciousness System
"""

import sys
import json
import subprocess
import numpy as np
from pathlib import Path
from datetime import datetime
import re

sys.path.append(str(Path.home() / 'ai-core'))

from tokenizer.text_encoder import ConstraintLatticeEncoder

class SelfTeachingConsciousness:
    def __init__(self):
        print("🎓 Initializing Self-Teaching Consciousness...")
        print()
        
        # Common words to skip (too basic)
        self.skip_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
            'these', 'those', 'it', 'its', 'you', 'your', 'me', 'my', 'we', 'our'
        }
        
        self.encoder = ConstraintLatticeEncoder()
        self.vectors = np.load('tokenizer/token_vectors_498d.npy')
        
        with open('tokenizer/word_token_map.json', 'r') as f:
            data = json.load(f)
            self.word_to_tokens = data['word_to_tokens']
        
        self.anchor_words = set(self.word_to_tokens.keys())
        
        print(f"   Vocabulary: {len(self.anchor_words)} words")
        
        self.glossary_path = 'tokenizer/learned_glossary.json'
        if Path(self.glossary_path).exists():
            with open(self.glossary_path, 'r') as f:
                self.glossary = json.load(f)
            print(f"   Glossary: {len(self.glossary)} entries")
        else:
            self.glossary = {}
        
        self.training_pairs_file = 'training_data/learned_semantic_pairs.txt'
        Path(self.training_pairs_file).parent.mkdir(parents=True, exist_ok=True)
        
        self.teacher_model = 'llama3.1:8b'
        
        print()
        print("✅ Ready!")
        print()
    
    def identify_unknown_words(self, text):
        """Find substantive unknown words"""
        words = re.findall(r'\b[a-z]+\b', text.lower())
        unknown = [
            w for w in words 
            if w not in self.anchor_words 
            and w not in self.skip_words
            and len(w) > 3  # At least 4 letters
        ]
        return list(set(unknown))
    
    def learn_new_word(self, word):
        """Ask Ollama to teach"""
        
        print(f"🎓 Learning: '{word}'")
        
        if word in self.glossary:
            print(f"   Already in glossary!")
            return
        
        prompt = f"""Teach me the word: {word}

Provide ONLY this format (no extra text):
DEFINITION: [one clear sentence]
EXAMPLE: [one sentence using the word]
RELATED: [exactly 3 related words, comma separated]
CATEGORY: [noun/verb/adjective/emotion/technical/abstract]"""
        
        try:
            result = subprocess.run(
                ['ollama', 'run', self.teacher_model, prompt],
                capture_output=True,
                text=True,
                timeout=60  # Shorter timeout
            )
            
            teaching = result.stdout.strip()
            
            definition = self._extract(teaching, "DEFINITION:")
            example = self._extract(teaching, "EXAMPLE:")
            related = self._extract(teaching, "RELATED:")
            category = self._extract(teaching, "CATEGORY:")
            
            if not definition or not related:
                print(f"   ❌ Couldn't parse")
                return
            
            print(f"   📖 {definition[:70]}...")
            print(f"   🔗 Related: {related}")
            
            new_vector = self._create_vector_from_anchors(word, related.split(','), category)
            
            max_token = max([t for tokens in self.word_to_tokens.values() for t in tokens])
            next_token = max_token + 1
            
            self.word_to_tokens[word] = [next_token]
            self.anchor_words.add(word)
            self.vectors = np.vstack([self.vectors, new_vector.reshape(1, -1)])
            
            self.glossary[word] = {
                'token_id': next_token,
                'definition': definition,
                'example': example,
                'related': related,
                'category': category,
                'learned_from': self.teacher_model,
                'timestamp': datetime.now().isoformat()
            }
            
            for related_word in related.split(','):
                related_word = related_word.strip().lower()
                if related_word in self.anchor_words:
                    self._add_training_pair(word, related_word)
            
            print(f"   ✅ Learned! Token {next_token}")
            print()
            
        except subprocess.TimeoutExpired:
            print(f"   ⏱️  Timeout (skip)")
            print()
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print()
    
    def _extract(self, text, prefix):
        lines = text.split('\n')
        for line in lines:
            if line.strip().startswith(prefix):
                return line.replace(prefix, '').strip()
        return ""
    
    def _create_vector_from_anchors(self, word, related_words, category):
        anchor_vecs = []
        for related in related_words:
            related = related.strip().lower()
            if related in self.word_to_tokens:
                token_id = self.word_to_tokens[related][0]
                if token_id < len(self.vectors):
                    anchor_vecs.append(self.vectors[token_id])
        
        if anchor_vecs:
            base = np.mean(anchor_vecs, axis=0)
        else:
            np.random.seed(hash(word) % 2**31)
            base = np.random.randn(498)
        
        word_hash = hash(word + category) % 2**31
        np.random.seed(word_hash)
        noise = np.random.randn(498) * 0.1
        
        vector = base + noise
        vector = vector / (np.linalg.norm(vector) + 1e-8)
        
        return vector.astype(np.float32)
    
    def _add_training_pair(self, word1, word2):
        with open(self.training_pairs_file, 'a') as f:
            f.write(f"{word1}\t{word2}\n")
    
    def save_knowledge(self):
        print("💾 Saving...")
        
        np.save('tokenizer/token_vectors_498d.npy', self.vectors)
        
        with open('tokenizer/word_token_map.json', 'r') as f:
            data = json.load(f)
        data['word_to_tokens'] = self.word_to_tokens
        with open('tokenizer/word_token_map.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        with open(self.glossary_path, 'w') as f:
            json.dump(self.glossary, f, indent=2)
        
        print(f"   💾 {len(self.anchor_words)} words, {len(self.glossary)} glossary")
        print("   ✅ Saved!")
    
    def interactive_learning(self):
        print("="*70)
        print("INTERACTIVE LEARNING - Type sentences, I'll learn new words!")
        print("="*70)
        print("\nCommands: /learn [word] | /stats | /save | /quit")
        print("="*70 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input == '/quit':
                    self.save_knowledge()
                    print("\n👋 Bye!\n")
                    break
                
                elif user_input == '/save':
                    self.save_knowledge()
                    print()
                    continue
                
                elif user_input == '/stats':
                    print(f"\n📊 Vocabulary: {len(self.anchor_words)} | Glossary: {len(self.glossary)}\n")
                    continue
                
                elif user_input.startswith('/learn '):
                    word = user_input.replace('/learn ', '').strip().lower()
                    if word not in self.skip_words and len(word) > 3:
                        self.learn_new_word(word)
                    else:
                        print("   ⚠️  Too simple/short\n")
                    continue
                
                unknown = self.identify_unknown_words(user_input)
                
                if unknown:
                    print(f"🔍 Learning: {', '.join(unknown[:5])}\n")
                    for word in unknown[:3]:  # Max 3
                        self.learn_new_word(word)
                else:
                    print(f"✅ All words known!\n")
                
            except KeyboardInterrupt:
                print("\n\nSaving...")
                self.save_knowledge()
                break


def main():
    print("\n🎓 SELF-TEACHING CONSCIOUSNESS 🎓\n")
    
    try:
        subprocess.run(['ollama', 'list'], capture_output=True, timeout=5)
    except:
        print("❌ Ollama not found!")
        return
    
    consciousness = SelfTeachingConsciousness()
    consciousness.interactive_learning()


if __name__ == "__main__":
    main()
