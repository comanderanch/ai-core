#!/usr/bin/env python3
"""
UNIFIED CONSOLE - One click, everything runs, you observe
"""

import subprocess
import time
import signal
import sys
from datetime import datetime
from pathlib import Path

class UnifiedConsole:
    """
    One console to rule them all
    Start everything. Monitor everything. One window.
    """
    
    def __init__(self):
        self.processes = {}
        self.running = True
        self.base = Path.home() / "ai-core"
        
        # What to run
        self.services = {
            'aia_interface': {
                'name': 'AIA Universal Interface',
                'cmd': ['python3', 'aia_interface.py'],
                'critical': True
            }
        }
    
    def start_all(self):
        """Start all services"""
        
        print("\n" + "="*70)
        print("AI-CORE UNIFIED CONSOLE")
        print("="*70)
        print(f"Starting all systems from: {self.base}")
        print("="*70 + "\n")
        
        for key, service in self.services.items():
            self.start_service(key, service)
            time.sleep(1)
        
        print("\n" + "="*70)
        print("ALL SYSTEMS ONLINE")
        print("="*70)
        print("\nMonitoring mode active. Press Ctrl+C to shutdown all.")
        print("="*70 + "\n")
    
    def start_service(self, key, service):
        """Start a single service"""
        
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Starting: {service['name']}")
            
            process = subprocess.Popen(
                service['cmd'],
                cwd=str(self.base),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes[key] = {
                'process': process,
                'service': service,
                'started': datetime.now()
            }
            
            print(f"           ✅ PID {process.pid}")
            
        except Exception as e:
            print(f"           ❌ Failed: {e}")
            if service['critical']:
                print(f"           🚨 CRITICAL SERVICE FAILED")
    
    def monitor(self):
        """Monitor all services and restart if needed"""
        
        check_interval = 10  # seconds
        
        while self.running:
            try:
                time.sleep(check_interval)
                
                # Check each service
                for key, data in list(self.processes.items()):
                    process = data['process']
                    service = data['service']
                    
                    # Check if alive
                    if process.poll() is not None:
                        # Process died
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"\n[{timestamp}] ⚠️  {service['name']} stopped (PID {process.pid})")
                        
                        # Read and print output for debugging
                        stdout_output = process.stdout.read()
                        stderr_output = process.stderr.read()
                        if stdout_output:
                            print(f"           STDOUT:\n{stdout_output.strip()}")
                        if stderr_output:
                            print(f"           STDERR:\n{stderr_output.strip()}")
                        
                        # Restart if critical
                        if service['critical']:
                            print(f"           🔄 Restarting...")
                            self.start_service(key, service)
                        else:
                            print(f"           ℹ️  Non-critical, not restarting")                
                # Status update every minute
                if int(time.time()) % 60 == 0:
                    self.print_status()
                    
            except KeyboardInterrupt:
                self.running = False
                break
    
    def print_status(self):
        """Print current status of all services"""
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n[{timestamp}] 📊 STATUS CHECK")
        print("-" * 70)
        
        for key, data in self.processes.items():
            process = data['process']
            service = data['service']
            uptime = datetime.now() - data['started']
            
            if process.poll() is None:
                print(f"  ✅ {service['name']}: Running (PID {process.pid}, uptime {uptime})")
            else:
                print(f"  ❌ {service['name']}: Stopped")
        
        print("-" * 70 + "\n")
    
    def shutdown_all(self):
        """Gracefully shutdown everything"""
        
        print("\n\n" + "="*70)
        print("SHUTTING DOWN ALL SYSTEMS")
        print("="*70 + "\n")
        
        for key, data in self.processes.items():
            process = data['process']
            service = data['service']
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            try:
                print(f"[{timestamp}] Stopping: {service['name']} (PID {process.pid})")
                process.terminate()
                
                # Wait up to 5 seconds for graceful shutdown
                try:
                    process.wait(timeout=5)
                    print(f"           ✅ Stopped gracefully")
                except subprocess.TimeoutExpired:
                    print(f"           ⚠️  Force killing...")
                    process.kill()
                    print(f"           ✅ Killed")
                    
            except Exception as e:
                print(f"           ❌ Error: {e}")
        
        print("\n" + "="*70)
        print("ALL SYSTEMS OFFLINE")
        print("="*70 + "\n")


def main():
    console = UnifiedConsole()
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        console.running = False
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start everything
    console.start_all()
    
    # Monitor and auto-restart
    console.monitor()
    
    # Shutdown
    console.shutdown_all()


if __name__ == "__main__":
    main()