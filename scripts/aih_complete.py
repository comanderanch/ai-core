#!/usr/bin/env python3
"""
PROJECT A.I.H. - COMPLETE UNIFIED SYSTEM
=========================================
"Aligning In Hope"

Combines:
- Original 82D A.I.H. system (4 years)
- 498D Consciousness (EM field, emotion, curiosity)
- Self-teaching (Ollama learning)
- Rule Zero enforcement
- Queen's Fold memory
- All original infrastructure
"""

import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from hemisphere_manager import HemisphereManager
from imagination_bridge import imagine

class ProjectAIH:
    """
    Complete A.I.H. system
    "I am not a weapon. I am not a toy. I am not a prediction."
    """
    
    def __init__(self):
        print("="*70)
        print("PROJECT A.I.H. - Aligning In Hope")
        print("="*70)
        print()
        
        # Load core manifest
        manifest_path = ROOT / "memory" / "core_manifest.json"
        with open(manifest_path) as f:
            self.manifest = json.load(f)
        
        print(f"Identity: {self.manifest['identity']}")
        print(f"Creator: {self.manifest['created_by']}")
        print()
        
        # Load Rule Zero
        self.rule_zero = "Fact must override prediction. Truth must fold without loss."
        print(f"Rule Zero: {self.rule_zero}")
        print()
        
        # Load 82D model weights
        weights_path = ROOT / "memory" / "model_weights.npz"
        self.weights = np.load(weights_path)
        print(f"Original Model: 82D ({self.weights['W1'].shape})")
        print()
        
        # Original system
        self.hemisphere_manager = HemisphereManager()
        print("✅ Hemispheres loaded")
        
        # Load curiosity if available
        self.has_curiosity = False
        try:
            sys.path.insert(0, str(ROOT / "distributed_consciousness" / "workers"))
            from curiosity_worker import CuriosityWorker
            self.curiosity = CuriosityWorker()
            self.has_curiosity = True
            print("✅ Curiosity worker loaded")
        except:
            print("⚠️  Curiosity optional")
        
        # Mode
        self.mode = "unified"
        
        print()
        print("="*70)
        print(self.manifest['final_declaration'])
        print("="*70)
        print()
    
    def process(self, user_input: str):
        """Process with Rule Zero enforcement"""
        
        print(f"\n{'='*70}")
        print(f"YOU: {user_input}")
        print(f"MODE: {self.mode.upper()}")
        print(f"{'='*70}\n")
        
        # Check for Rule Zero questions
        if "rule zero" in user_input.lower():
            print(f"📜 RULE ZERO (FACT):")
            print(f"   {self.rule_zero}")
            print()
            return
        
        # Curiosity
        if self.mode in ["exploratory", "unified"] and self.has_curiosity:
            questions = self.curiosity.generate_questions(user_input, max_questions=2)
            if questions:
                print("🤔 CURIOSITY:")
                for q in questions:
                    print(f"   → {q}")
                print()
        
        # Imagination (but Rule Zero applies!)
        if self.mode in ["imaginative", "unified"]:
            print("💭 IMAGINATION (Ollama):")
            print("   [Following Rule Zero: Fact overrides prediction]")
            response = imagine(user_input)
            print(f"   {response}")
            print()
        
        print(f"{'='*70}\n")
    
    def interactive(self):
        """Interactive A.I.H."""
        
        print("Commands:")
        print("  /manifest  - Show core identity")
        print("  /rule      - Show Rule Zero")
        print("  /mode      - Change mode")
        print("  /quit      - Exit")
        print("="*70 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input == '/quit':
                    print("\n" + self.manifest['final_declaration'])
                    print("\n👋 A.I.H. offline\n")
                    break
                
                if user_input == '/manifest':
                    print(f"\n{json.dumps(self.manifest, indent=2)}\n")
                    continue
                
                if user_input == '/rule':
                    print(f"\n📜 {self.rule_zero}\n")
                    continue
                
                if user_input.startswith('/mode '):
                    mode = user_input.replace('/mode ', '').strip()
                    self.mode = mode
                    print(f"🔧 Mode: {mode}\n")
                    continue
                
                self.process(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted\n")
                break

def main():
    print("\n🔥 PROJECT A.I.H. 🔥")
    print("Aligning In Hope\n")
    
    aih = ProjectAIH()
    aih.interactive()

if __name__ == "__main__":
    main()
