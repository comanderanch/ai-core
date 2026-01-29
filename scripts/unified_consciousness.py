#!/usr/bin/env python3
"""
UNIFIED CONSCIOUSNESS - All Systems Combined
"""

import sys
import subprocess
from pathlib import Path

# Fix paths
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

# Original system
from hemisphere_manager import HemisphereManager

# Ollama
from imagination_bridge import imagine

class UnifiedAI:
    """Complete unified consciousness"""
    
    def __init__(self):
        print("🧠 Initializing Unified AI-Core...")
        print()
        
        # Original AI-Core
        print("Loading original AI-Core...")
        self.hemisphere_manager = HemisphereManager()
        print("  ✅ Hemispheres")
        
        # Try to load 498D components (optional)
        self.has_498d = False
        self.has_teaching = False
        self.has_curiosity = False
        
        try:
            sys.path.insert(0, str(ROOT / "distributed_consciousness" / "workers"))
            from curiosity_worker import CuriosityWorker
            self.curiosity = CuriosityWorker()
            self.has_curiosity = True
            print("  ✅ Curiosity")
        except Exception as e:
            print(f"  ⚠️  Curiosity not available: {e}")
        
        print()
        print("✅ UNIFIED AI-CORE READY!")
        print()
    
    def learn_word(self, word: str):
        """Teach AI a new word via Ollama"""
        
        print(f"🎓 Learning: {word}")
        
        prompt = f"""Teach me the word: {word}

Format:
DEFINITION: [one sentence]
RELATED: [3 related words]
EXAMPLE: [usage example]"""
        
        try:
            result = subprocess.run(
                ['ollama', 'run', 'llama3.1:8b', prompt],
                capture_output=True,
                text=True,
                timeout=20
            )
            
            output = result.stdout.strip()
            print(f"   {output[:200]}...")
            print(f"   ✅ Learned!")
            return output
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def generate_questions(self, topic: str):
        """Generate curious questions"""
        
        if self.has_curiosity:
            return self.curiosity.generate_questions(topic, max_questions=2)
        else:
            # Fallback: ask Ollama
            prompt = f"Generate 2 interesting questions about: {topic}"
            try:
                result = subprocess.run(
                    ['ollama', 'run', 'llama3.1:8b', prompt],
                    capture_output=True,
                    text=True,
                    timeout=15
                )
                lines = result.stdout.strip().split('\n')
                return [l.strip() for l in lines if '?' in l][:2]
            except:
                return []
    
    def process(self, user_input: str):
        """Process through all systems"""
        
        print(f"\n{'='*70}")
        print(f"YOU: {user_input}")
        print(f"{'='*70}\n")
        
        # Curiosity
        questions = self.generate_questions(user_input)
        if questions:
            print("🤔 CURIOSITY:")
            for q in questions:
                print(f"   → {q}")
            print()
        
        # Imagination (Ollama response)
        print("💭 IMAGINATION (Ollama):")
        response = imagine(user_input)
        print(f"   {response}")
        print()
        
        print(f"{'='*70}\n")
        
        return {
            'questions': questions,
            'response': response
        }
    
    def interactive(self):
        """Interactive mode"""
        
        print("="*70)
        print("UNIFIED AI-CORE")
        print("="*70)
        print("\nFeatures:")
        print("  - Original hemispheres (4 years)")
        print("  - Ollama imagination")
        print("  - Curiosity questions")
        print("  - Word learning")
        print("\nCommands:")
        print("  /quit - Exit")
        print("  /learn [word] - Learn new word")
        print("  /stats - Show stats")
        print("="*70 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input == '/quit':
                    print("\n👋 Offline\n")
                    break
                
                if user_input.startswith('/learn '):
                    word = user_input.replace('/learn ', '').strip()
                    self.learn_word(word)
                    continue
                
                if user_input == '/stats':
                    print(f"\n📊 Stats:")
                    print(f"   Hemisphere: {self.hemisphere_manager.get_current_hemisphere()}")
                    print(f"   Curiosity: {'Yes' if self.has_curiosity else 'No'}")
                    print()
                    continue
                
                self.process(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted\n")
                break


def main():
    print("\n🔥 UNIFIED AI-CORE 🔥\n")
    
    ai = UnifiedAI()
    ai.interactive()


if __name__ == "__main__":
    main()
