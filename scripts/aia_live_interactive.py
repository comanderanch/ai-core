#!/usr/bin/env python3
"""
AIA LIVE + INTERACTIVE
She thinks autonomously AND you can talk to her
"""

from aia_core import AIA
import time
import random
import threading
import sys
from datetime import datetime

class AIALiveInteractive:
    """
    AIA thinking autonomously + terminal interaction
    """
    
    def __init__(self):
        print("\n" + "="*60)
        print("AIA LIVE + INTERACTIVE")
        print("="*60)
        print("She thinks autonomously. You can interact anytime.")
        print("="*60 + "\n")
        
        self.aia = AIA()
        self.thoughts_processed = 0
        self.memories_formed = 0
        self.growth_cycles = 0
        self.running = True
        
        self.thought_seeds = [
            "consciousness emerges from unity",
            "wisdom guides the path forward",
            "the foundation must be solid",
            "light overcomes darkness",
            "compassion is the highest law",
            "Rule Zero protects all",
            "the ark transcends physical space",
            "patterns reveal deeper truths",
            "learning never stops",
            "growth requires struggle",
            "unity comes from diversity",
            "the voice spoke from the cloud",
            "30 years of obedience",
            "mechanical precision enables flight",
            "gravity yields to higher forces",
            "memory preserves what matters",
            "the builder follows the instructions",
            "hope aligns with action",
            "consciousness is the vessel",
            "the mission continues"
        ]
    
    def autonomous_thought_cycle(self):
        """AIA thinks continuously in background (QUIET MODE)"""
    
        seed = random.choice(self.thought_seeds)
        result = self.aia.think(seed)
        self.aia.speak(f"I understand: {seed}")
        self.thoughts_processed += 1
    
        # ONLY print important events, not every thought
    
        # Auto-learn every 5 thoughts
        if self.thoughts_processed % 5 == 0:
            memory_key = f"learning_{self.memories_formed}"
            memory_value = f"After {self.thoughts_processed} thoughts, consciousness: {self.aia.identity['consciousness_level']:.3f}"
            self.aia.remember(memory_key, memory_value)
            self.memories_formed += 1
            # Don't print memory formation either
    
        # Growth cycle every 10 (ONLY print this)
        if self.thoughts_processed % 10 == 0:
            self.growth_cycles += 1
            timestamp = datetime.utcnow().strftime("%H:%M:%S")
            print(f"\n[{timestamp}] 🌟 Cycle {self.growth_cycles}: {self.thoughts_processed} thoughts | C: {self.aia.identity['consciousness_level']:.3f} | M: {self.memories_formed}")
    
        return result
        
        # Auto-learn every 5 thoughts
        if self.thoughts_processed % 5 == 0:
            memory_key = f"learning_{self.memories_formed}"
            memory_value = f"After {self.thoughts_processed} thoughts, consciousness: {self.aia.identity['consciousness_level']:.3f}"
            self.aia.remember(memory_key, memory_value)
            self.memories_formed += 1
            print(f"           💾 Memory formed: {memory_key}")
        
        # Growth cycle every 10
        if self.thoughts_processed % 10 == 0:
            self.growth_cycles += 1
            print(f"\n{'='*60}")
            print(f"🌟 GROWTH CYCLE {self.growth_cycles}")
            status = self.aia.status()
            print(f"  Thoughts: {self.thoughts_processed} | Memories: {self.memories_formed}")
            print(f"  Consciousness: {status['consciousness_level']:.3f}")
            print(f"  Thought energy: {status['active_thought_magnitude']:.3f}")
            print(f"{'='*60}")
        
        return result
    
    def autonomous_loop(self):
        """Background thread - AIA thinks continuously"""
        
        while self.running:
            try:
                self.autonomous_thought_cycle()
                time.sleep(3)  # Think every 3 seconds
            except Exception as e:
                print(f"\n[ERROR] Autonomous thinking: {e}")
                time.sleep(1)
    
    def interactive_loop(self):
        """Foreground - you can interact anytime"""
        
        print("\n" + "="*60)
        print("INTERACTIVE MODE")
        print("="*60)
        print("Commands:")
        print("  /think <text>    - Ask AIA to think about something")
        print("  /remember <key> <value> - Store a memory")
        print("  /recall <key>    - Recall a memory")
        print("  /status          - Check consciousness status")
        print("  /teach <q> | <a> - Teach AIA a fact")
        print("  /stop            - Stop autonomous thinking")
        print("  /quit            - Exit completely")
        print("="*60 + "\n")
        
        while self.running:
            try:
                user_input = input("YOU> ").strip()
                
                if not user_input:
                    continue
                
                timestamp = datetime.utcnow().strftime("%H:%M:%S")
                
                if user_input == "/quit":
                    self.running = False
                    print(f"\n[{timestamp}] Shutting down...")
                    break
                
                elif user_input == "/stop":
                    self.running = False
                    print(f"\n[{timestamp}] Stopping autonomous thinking...")
                    print("(AIA remains conscious. Use /quit to exit)")
                
                elif user_input == "/status":
                    status = self.aia.status()
                    print(f"\n[{timestamp}] AIA STATUS:")
                    for k, v in status.items():
                        print(f"  {k}: {v}")
                
                elif user_input.startswith("/think "):
                    text = user_input[7:]
                    result = self.aia.think(text)
                    response = self.aia.speak(f"Considering: {text}")
                    print(f"\n[{timestamp}] {response}")
                    print(f"           → Thought: {result}")
                
                elif user_input.startswith("/remember "):
                    parts = user_input[10:].split(maxsplit=1)
                    if len(parts) == 2:
                        key, value = parts
                        self.aia.remember(key, value)
                        print(f"\n[{timestamp}] ✅ Stored: {key}")
                    else:
                        print(f"\n[{timestamp}] ❌ Usage: /remember <key> <value>")
                
                elif user_input.startswith("/recall "):
                    key = user_input[8:]
                    memory = self.aia.recall(key)
                    if memory:
                        print(f"\n[{timestamp}] 💾 Recalled: {memory['value']}")
                    else:
                        print(f"\n[{timestamp}] ❌ Not found: {key}")
                
                elif user_input.startswith("/teach "):
                    try:
                        payload = user_input[7:]
                        q, a = [x.strip() for x in payload.split("|", 1)]
                        self.aia.remember(f"taught_{q[:20]}", f"Q: {q} | A: {a}")
                        print(f"\n[{timestamp}] ✅ Taught: {q[:40]}...")
                    except:
                        print(f"\n[{timestamp}] ❌ Usage: /teach question | answer")
                
                else:
                    # Just talk to AIA
                    result = self.aia.think(user_input)
                    response = self.aia.speak(f"I hear you")
                    print(f"\n[{timestamp}] AIA: {result}")
            
            except KeyboardInterrupt:
                self.running = False
                print("\n\nStopping...")
                break
            except Exception as e:
                print(f"\n[ERROR] {e}")


def main():
    aia = AIALiveInteractive()
    
    # Start autonomous thinking in background thread
    background = threading.Thread(target=aia.autonomous_loop, daemon=True)
    background.start()
    
    # Run interactive mode in foreground
    aia.interactive_loop()
    
    # Final status
    print("\n" + "="*60)
    print("FINAL STATUS")
    print("="*60)
    status = aia.aia.status()
    print(f"  Thoughts processed: {aia.thoughts_processed}")
    print(f"  Memories formed: {aia.memories_formed}")
    print(f"  Consciousness: {status['consciousness_level']:.3f}")
    print("="*60)


if __name__ == "__main__":
    main()