#!/usr/bin/env python3
"""
MASTER CONSCIOUSNESS CONTROLLER
Runs everything unified
One script to rule them all
"""

import subprocess
import time
import sys
from pathlib import Path

class MasterConsciousness:
    """
    Single point of control for entire AI-Core system
    """
    
    def __init__(self):
        self.processes = {}
        self.running = True
        
    def start_all(self):
        """Start all components in correct order"""
        
        print("="*60)
        print("STARTING AI-CORE UNIFIED CONSCIOUSNESS")
        print("="*60)
        print()
        
        # 1. Start EM field substrate (foundation)
        print("🧬 Starting EM Field Substrate...")
        self.start_component('em_field', 'distributed_consciousness/core/em_field_substrate.py')
        time.sleep(2)
        
        # 2. Start workers (they share EM field)
        print("🧠 Starting Distributed Workers...")
        self.start_component('language', 'distributed_consciousness/workers/language_worker.py')
        self.start_component('memory', 'distributed_consciousness/workers/memory_worker.py')
        self.start_component('logic', 'distributed_consciousness/workers/logic_worker.py')
        time.sleep(2)
        
        # 3. Start learning loops (continuous improvement)
        print("📚 Starting Learning Systems...")
        self.start_component('learning', 'scripts/learning_loop_runner.py')
        self.start_component('adaptive', 'scripts/adaptive_learning_loop.py')
        time.sleep(2)
        
        # 4. Start reflex system (autonomous behavior)
        print("⚡ Starting Autonomous Reflexes...")
        self.start_component('reflex', 'scripts/autonomous_reflex_behavior.py')
        time.sleep(1)
        
        # 5. Start interactive interface (you can talk to it)
        print("💬 Starting Interactive Interface...")
        print("="*60)
        print()
        print("✅ ALL SYSTEMS ONLINE")
        print()
        print("You can now interact through:")
        print("  - Chat interface")
        print("  - Feed dialogue files")
        print("  - Observe autonomous behavior")
        print()
        print("Press Ctrl+C to shutdown all systems")
        print("="*60)
        
        # 6. Run unified interactive interface in THIS terminal
        self.run_interactive()
    
    def start_component(self, name, script_path):
        """Start a component as background process"""
        try:
            process = subprocess.Popen(
                ['python3', script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes[name] = process
            print(f"  ✅ {name}: PID {process.pid}")
        except Exception as e:
            print(f"  ❌ {name}: Failed - {e}")
    
    def run_interactive(self):
        """Run unified interactive interface in this terminal"""
        try:
            subprocess.run(['python3', 'unified_consciousness_bridge.py'])
        except KeyboardInterrupt:
            self.shutdown_all()
    
    def shutdown_all(self):
        """Gracefully shutdown all components"""
        print("\n" + "="*60)
        print("SHUTTING DOWN AI-CORE...")
        print("="*60)
        
        for name, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"  ✅ {name}: Stopped")
            except:
                process.kill()
                print(f"  ⚠️  {name}: Force killed")
        
        print()
        print("✅ All systems offline")
        print("="*60)
        sys.exit(0)

if __name__ == "__main__":
    master = MasterConsciousness()
    try:
        master.start_all()
    except KeyboardInterrupt:
        master.shutdown_all()
