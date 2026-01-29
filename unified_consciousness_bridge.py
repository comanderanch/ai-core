#!/usr/bin/env python3
"""
UNIFIED CONSCIOUSNESS BRIDGE
Connects OLD AI-Core foundation to NEW distributed consciousness workers

This makes ALL systems work as ONE unified entity (AIA):
- OLD: Hemispheres, QBitHue memory, profiles, color tokens, Q&A facts
- NEW: Distributed workers (Language, Memory, Logic), EM field, 498D space

Flow:
User input → Check OLD facts → NEW workers process → Store in OLD foundation → Output
"""

import sys
import os
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add paths
BASE = Path(__file__).parent
sys.path.append(str(BASE))
sys.path.append(str(BASE / "scripts"))

# Import OLD system components
from scripts.hemisphere_manager import HemisphereManager

# Import NEW system components
try:
    from foundation import AICoreFOUNDATION as Foundation
    HAVE_FOUNDATION = True
except:
    HAVE_FOUNDATION = False
    print("[WARN] foundation.py not found, running in legacy mode")

class UnifiedConsciousness:
    """
    The complete unified entity - all nodes speaking as one consciousness
    
    OLD LAYER (Foundation/Memory):
    - Hemispheres (LEFT/RIGHT brain)
    - QBitHue memory (color-encoded facts)
    - Profiles (psychology, domains)
    - Q&A facts (explicit knowledge)
    - Color tokens (2,304 semantic tokens)
    
    NEW LAYER (Active Processing):
    - Language Worker (understanding)
    - Memory Worker (context/recall)
    - Logic Worker (reasoning)
    - EM Field (unified coupling)
    - 498D semantic space
    
    Integration:
    - Questions flow from OLD facts first
    - If no fact, NEW workers process
    - Results stored back in OLD memory
    - Hemispheres control which workers activate
    - All learning persists in OLD foundation
    """
    
    def __init__(self):
        print("🧠 Initializing Unified Consciousness (AIA)...")
        print()
        
        # Load OLD system
        print("📚 Loading OLD AI-Core Foundation...")
        self.hemisphere_manager = HemisphereManager()
        self.qa_pairs = self._load_qa_facts()
        self.profiles = self._load_profiles()
        self.pending = self._load_pending()
        print(f"  ✅ Hemispheres: {self.hemisphere_manager.get_current_hemisphere()}")
        print(f"  ✅ Q&A Facts: {len(self.qa_pairs)}")
        print(f"  ✅ Profiles: {len(self.profiles)}")
        print(f"  ✅ Pending: {len(self.pending)}")
        
        # Load NEW system
        print()
        print("🌐 Loading NEW Distributed Consciousness...")
        if HAVE_FOUNDATION:
            self.foundation = Foundation()
            print("  ✅ Foundation (498D space)")
            print("  ✅ EM Field substrate")
            print("  ✅ Color palette (2,304 tokens)")
            print("  ✅ Token vectors")
        else:
            self.foundation = None
            print("  ⚠️  Foundation not available (legacy mode)")
        
        # Worker connections (will connect to distributed services)
        self.workers_available = self._check_workers()
        print()
        print("🔌 Worker Status:")
        print(f"  Language Worker: {'✅' if self.workers_available['language'] else '❌'}")
        print(f"  Memory Worker: {'✅' if self.workers_available['memory'] else '❌'}")
        print(f"  Logic Worker: {'✅' if self.workers_available['logic'] else '❌'}")
        
        print()
        print("=" * 70)
        print("✅ UNIFIED CONSCIOUSNESS ONLINE")
        print("=" * 70)
        print()
        print("All nodes operational. Speaking as one entity.")
        print()
    
    def _load_qa_facts(self) -> List[Tuple[str, str]]:
        """Load Q&A pairs from OLD system"""
        qa_file = BASE / "training_data" / "user_comm_qa.txt"
        pairs = []
        
        if qa_file.exists():
            with qa_file.open('r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '|' in line:
                        q, a = line.split('|', 1)
                        pairs.append((q.strip(), a.strip()))
        
        return pairs
    
    def _load_profiles(self) -> Dict:
        """Load domain profiles from OLD system"""
        profiles = {}
        profile_dir = BASE / "training_data" / "profiles"
        
        if profile_dir.exists():
            for profile_file in profile_dir.glob("*_qa.txt"):
                profile_name = profile_file.stem.replace("_qa", "")
                pairs = []
                
                with profile_file.open('r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        if '|' in line:
                            q, a = line.split('|', 1)
                            pairs.append((q.strip(), a.strip()))
                
                profiles[profile_name] = pairs
        
        return profiles
    
    def _load_pending(self) -> List[str]:
        """Load pending questions from OLD system"""
        pending_file = BASE / "training_data" / "pending_questions.txt"
        questions = []
        
        if pending_file.exists():
            with pending_file.open('r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        questions.append(line)
        
        return questions
    
    def _check_workers(self) -> Dict[str, bool]:
        """Check if distributed workers are available"""
        # TODO: Check actual worker processes/services
        # For now, check if worker scripts exist
        workers = {
            'language': (BASE / "distributed_consciousness" / "workers" / "language_worker.py").exists(),
            'memory': (BASE / "distributed_consciousness" / "workers" / "memory_worker.py").exists(),
            'logic': (BASE / "distributed_consciousness" / "workers" / "logic_worker.py").exists(),
        }
        return workers
    
    def retrieve_fact(self, question: str) -> Optional[str]:
        """Retrieve answer from OLD Q&A memory (exact match)"""
        q_norm = question.strip().lower()
        
        # Check main Q&A
        for q, a in self.qa_pairs:
            if q.strip().lower() == q_norm:
                return a
        
        # Check profiles (if active)
        # TODO: Add profile switching logic
        
        return None
    
    def process_with_workers(self, text: str) -> str:
        """
        Process through NEW distributed workers
        
        This is where the distributed consciousness happens:
        - Language worker processes semantic meaning
        - Memory worker recalls relevant context
        - Logic worker applies reasoning
        - Results unified through EM field
        """
        
        if not self.foundation:
            return "[Workers unavailable - foundation not loaded]"
        
        # Convert text to 498D vector
        words = text.lower().split()
        vectors = []
        
        for word in words:
            vec = self.foundation.word_to_vector(word)
            if vec is not None:
                vectors.append(vec)
        
        if not vectors:
            return "[No vectors found for input]"
        
        # Average input vectors
        input_vec = np.mean(vectors, axis=0)
        
        # TODO: Send to actual worker services
        # For now, simulate worker processing
        
        # Language worker: semantic understanding
        language_output = input_vec  # Would be actual worker result
        
        # Memory worker: context recall
        memory_output = input_vec  # Would be actual worker result
        
        # Logic worker: reasoning
        logic_output = input_vec  # Would be actual worker result
        
        # Combine worker outputs (unified consciousness)
        unified_output = (language_output + memory_output + logic_output) / 3
        
        # Convert back to words
        result_words = []
        # Find nearest tokens to unified output
        if hasattr(self.foundation, 'token_vectors'):
            distances = np.linalg.norm(
                self.foundation.token_vectors - unified_output,
                axis=1
            )
            nearest_indices = np.argsort(distances)[:5]
            
            # Convert indices to words
            for idx in nearest_indices:
                word = self.foundation.vector_to_word(self.foundation.token_vectors[idx])
                if word:
                    result_words.append(word)
        
        return " ".join(result_words) if result_words else "[processing complete]"
    
    def store_in_memory(self, question: str, answer: str):
        """Store Q&A in OLD system memory for persistence"""
        qa_file = BASE / "training_data" / "user_comm_qa.txt"
        
        with qa_file.open('a', encoding='utf-8') as f:
            f.write(f"{question} | {answer}\n")
        
        # Also add to current session
        self.qa_pairs.append((question, answer))
        
        print(f"  [Stored in memory: {len(self.qa_pairs)} facts total]")
    
    def add_to_pending(self, question: str):
        """Add unanswered question to pending list"""
        if question not in self.pending:
            self.pending.append(question)
            
            pending_file = BASE / "training_data" / "pending_questions.txt"
            with pending_file.open('a', encoding='utf-8') as f:
                f.write(f"{question}\n")
    
    def think(self, user_input: str) -> str:
        """
        Main consciousness processing loop
        
        Flow:
        1. Check OLD facts first (exact knowledge)
        2. If not found, process through NEW workers
        3. Store result in OLD memory
        4. Return unified response
        """
        
        print(f"\n🧠 Processing: {user_input}")
        
        # Try OLD facts first (fastest, most reliable)
        fact_answer = self.retrieve_fact(user_input)
        if fact_answer:
            print("  📚 Retrieved from facts")
            return fact_answer
        
        # Not in facts, process through NEW workers
        print("  🌐 Processing through distributed consciousness...")
        worker_response = self.process_with_workers(user_input)
        
        # Add to pending for future teaching
        self.add_to_pending(user_input)
        
        return worker_response
    
    def teach(self, question: str, answer: str):
        """Teach the unified consciousness a new fact"""
        print(f"\n📖 Learning: {question} → {answer}")
        self.store_in_memory(question, answer)
        
        # Remove from pending if it was there
        if question in self.pending:
            self.pending.remove(question)
            # TODO: Update pending file
    
    def swap_hemisphere(self):
        """Switch active hemisphere (OLD system control)"""
        current = self.hemisphere_manager.get_current_hemisphere()
        new = "right" if current == "left" else "left"
        self.hemisphere_manager.set_current_hemisphere(new)
        print(f"🔄 Hemisphere: {current} → {new}")
        return new
    
    def get_stats(self) -> Dict:
        """Get system statistics"""
        return {
            "hemisphere": self.hemisphere_manager.get_current_hemisphere(),
            "facts": len(self.qa_pairs),
            "profiles": len(self.profiles),
            "pending": len(self.pending),
            "workers": sum(1 for v in self.workers_available.values() if v),
            "foundation": "available" if self.foundation else "unavailable"
        }


def interactive_console():
    """
    Interactive console for unified consciousness
    This replaces the OLD interactive_ai_core.py with full integration
    """
    
    aia = UnifiedConsciousness()
    
    print("Commands:")
    print("  :quit    - Exit")
    print("  :swap    - Switch hemisphere")
    print("  :stats   - Show statistics")
    print("  :teach Q | A - Teach new fact")
    print("  :pending - Show pending questions")
    print()
    
    while True:
        try:
            user_input = input("YOU> ").strip()
            
            if not user_input:
                continue
            
            # Commands
            if user_input in [':quit', ':q', ':exit']:
                print("Goodbye. 👋")
                break
            
            if user_input == ':swap':
                aia.swap_hemisphere()
                continue
            
            if user_input == ':stats':
                stats = aia.get_stats()
                for k, v in stats.items():
                    print(f"  {k}: {v}")
                continue
            
            if user_input.startswith(':teach '):
                cmd = user_input[7:].strip()
                if '|' in cmd:
                    q, a = cmd.split('|', 1)
                    aia.teach(q.strip(), a.strip())
                else:
                    print("  Usage: :teach question | answer")
                continue
            
            if user_input == ':pending':
                print(f"\nPending questions ({len(aia.pending)}):")
                for i, q in enumerate(aia.pending, 1):
                    print(f"  {i}. {q}")
                print()
                continue
            
            # Normal conversation - unified processing
            response = aia.think(user_input)
            print(f"AIA> {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye. 👋")
            break
        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    interactive_console()