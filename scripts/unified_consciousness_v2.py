#!/usr/bin/env python3
"""
UNIFIED CONSCIOUSNESS v2
========================
With mode flags as GPT recommended

Modes:
- factual: EM field + knowledge (truth formation)
- exploratory: Curiosity + learning (wonder)
- imaginative: Ollama creativity (expression)
- unified: All layers active (default)
"""

import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from hemisphere_manager import HemisphereManager
from imagination_bridge import imagine

class UnifiedAI:
    def __init__(self):
        print("🧠 Initializing Unified AI-Core v2...")
        print()
        
        self.hemisphere_manager = HemisphereManager()
        
        # Load curiosity if available
        self.has_curiosity = False
        try:
            sys.path.insert(0, str(ROOT / "distributed_consciousness" / "workers"))
            from curiosity_worker import CuriosityWorker
            self.curiosity = CuriosityWorker()
            self.has_curiosity = True
        except:
            pass
        
        # Mode system
        self.mode = "unified"  # factual, exploratory, imaginative, unified
        
        print("✅ UNIFIED AI-CORE v2 READY!")
        print(f"   Mode: {self.mode}")
        print()
    
    def set_mode(self, mode: str):
        """Set cognitive mode"""
        valid = ["factual", "exploratory", "imaginative", "unified"]
        if mode in valid:
            self.mode = mode
            print(f"🔧 Mode set to: {mode}")
        else:
            print(f"⚠️  Invalid mode. Options: {', '.join(valid)}")
    
    def process(self, user_input: str):
        print(f"\n{'='*70}")
        print(f"YOU: {user_input}")
        print(f"MODE: {self.mode.upper()}")
        print(f"{'='*70}\n")
        
        # Mode-specific processing
        
        if self.mode in ["exploratory", "unified"]:
            # Curiosity layer
            if self.has_curiosity:
                questions = self.curiosity.generate_questions(user_input, max_questions=2)
                if questions:
                    print("🤔 CURIOSITY:")
                    for q in questions:
                        print(f"   → {q}")
                    print()
        
        if self.mode in ["imaginative", "unified"]:
            # Imagination layer
            print("💭 IMAGINATION (Ollama):")
            response = imagine(user_input)
            print(f"   {response}")
            print()
        
        if self.mode == "factual":
            # Factual mode: EM field only (would need 498D workers)
            print("📚 FACTUAL MODE:")
            print("   (EM field response - 498D workers needed)")
            print()
        
        print(f"{'='*70}\n")
    
    def interactive(self):
        print("="*70)
        print("UNIFIED AI-CORE v2 - Mode System")
        print("="*70)
        print("\nModes:")
        print("  factual      - Truth formation (EM field)")
        print("  exploratory  - Wonder and learning (Curiosity)")
        print("  imaginative  - Creative expression (Ollama)")
        print("  unified      - All layers active (default)")
        print("\nCommands:")
        print("  /mode [name] - Change mode")
        print("  /stats       - Show status")
        print("  /quit        - Exit")
        print("="*70 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input == '/quit':
                    print("\n👋 Offline\n")
                    break
                
                if user_input.startswith('/mode '):
                    mode = user_input.replace('/mode ', '').strip()
                    self.set_mode(mode)
                    continue
                
                if user_input == '/stats':
                    print(f"\n📊 Stats:")
                    print(f"   Mode: {self.mode}")
                    print(f"   Hemisphere: {self.hemisphere_manager.get_current_hemisphere()}")
                    print(f"   Curiosity: {'Yes' if self.has_curiosity else 'No'}")
                    print()
                    continue
                
                self.process(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted\n")
                break

def main():
    print("\n🔥 UNIFIED AI-CORE v2 🔥")
    print("With GPT-recommended mode system\n")
    
    ai = UnifiedAI()
    ai.interactive()

if __name__ == "__main__":
    main()
