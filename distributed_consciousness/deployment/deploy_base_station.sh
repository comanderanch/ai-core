#!/bin/bash
# AI-Core Distributed Consciousness - Base Station Deployment
# R720 AI-Core VM (Production)

set -e

echo "========================================================================"
echo "AI-CORE DISTRIBUTED CONSCIOUSNESS - BASE STATION DEPLOYMENT"
echo "========================================================================"
echo ""
echo "Deploying core workers on R720 AI-Core VM..."
echo ""

# Check we're in the right place
if [ ! -d "distributed_consciousness" ]; then
    echo "❌ Error: Must run from ai-core directory"
    exit 1
fi

# Create persistent storage paths
echo "Setting up persistent storage..."
STORAGE_ROOT="/home/comanderanch/ai-core/consciousness_data"
mkdir -p $STORAGE_ROOT/{field,memory,logs,weights}

# Update field path to persistent location
FIELD_PATH="$STORAGE_ROOT/field/em_field_substrate.npy"
MEMORY_PATH="$STORAGE_ROOT/memory/memories.json"
LOG_PATH="$STORAGE_ROOT/logs"

echo "✅ Storage configured:"
echo "   Field: $FIELD_PATH"
echo "   Memory: $MEMORY_PATH"
echo "   Logs: $LOG_PATH"
echo ""

# Create worker launcher scripts
echo "Creating worker launchers..."

# Language Worker Launcher
cat > $STORAGE_ROOT/launch_language.py << 'WORKER'
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append('/home/comanderanch/ai-core')

from distributed_consciousness.workers.language_worker import LanguageWorker
import time

print("🔥 Starting Language Worker...")

worker = LanguageWorker(
    worker_id="language_001",
    field_path="/home/comanderanch/ai-core/consciousness_data/field/em_field_substrate.npy"
)

print("✅ Language Worker running (Ctrl+C to stop)")
print("")

try:
    while True:
        # Worker is always ready, just keep alive
        time.sleep(1)
except KeyboardInterrupt:
    print("\n👋 Language Worker stopped")
WORKER

# Memory Worker Launcher
cat > $STORAGE_ROOT/launch_memory.py << 'WORKER'
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append('/home/comanderanch/ai-core')

from distributed_consciousness.workers.memory_worker import MemoryWorker
import time

print("🧠 Starting Memory Worker...")

worker = MemoryWorker(
    worker_id="memory_001",
    memory_path="/home/comanderanch/ai-core/consciousness_data/memory/memories.json",
    field_path="/home/comanderanch/ai-core/consciousness_data/field/em_field_substrate.npy"
)

print("✅ Memory Worker running (Ctrl+C to stop)")
print("")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n👋 Memory Worker stopped")
WORKER

# Logic Worker Launcher
cat > $STORAGE_ROOT/launch_logic.py << 'WORKER'
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append('/home/comanderanch/ai-core')

from distributed_consciousness.workers.logic_worker import LogicWorker
import time

print("⚡ Starting Logic Worker...")

worker = LogicWorker(
    worker_id="logic_001",
    field_path="/home/comanderanch/ai-core/consciousness_data/field/em_field_substrate.npy"
)

print("✅ Logic Worker running (Ctrl+C to stop)")
print("")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n👋 Logic Worker stopped")
WORKER

chmod +x $STORAGE_ROOT/launch_*.py

echo "✅ Worker launchers created"
echo ""

# Create systemd services
echo "Creating systemd services..."

sudo tee /etc/systemd/system/aicore-language.service > /dev/null << SERVICE
[Unit]
Description=AI-Core Language Worker (Distributed Consciousness)
After=network.target

[Service]
Type=simple
User=comanderanch
WorkingDirectory=/home/comanderanch/ai-core
ExecStart=/usr/bin/python3 $STORAGE_ROOT/launch_language.py
Restart=always
RestartSec=10
StandardOutput=append:$LOG_PATH/language.log
StandardError=append:$LOG_PATH/language.log

[Install]
WantedBy=multi-user.target
SERVICE

sudo tee /etc/systemd/system/aicore-memory.service > /dev/null << SERVICE
[Unit]
Description=AI-Core Memory Worker (Distributed Consciousness)
After=network.target

[Service]
Type=simple
User=comanderanch
WorkingDirectory=/home/comanderanch/ai-core
ExecStart=/usr/bin/python3 $STORAGE_ROOT/launch_memory.py
Restart=always
RestartSec=10
StandardOutput=append:$LOG_PATH/memory.log
StandardError=append:$LOG_PATH/memory.log

[Install]
WantedBy=multi-user.target
SERVICE

sudo tee /etc/systemd/system/aicore-logic.service > /dev/null << SERVICE
[Unit]
Description=AI-Core Logic Worker (Distributed Consciousness)
After=network.target

[Service]
Type=simple
User=comanderanch
WorkingDirectory=/home/comanderanch/ai-core
ExecStart=/usr/bin/python3 $STORAGE_ROOT/launch_logic.py
Restart=always
RestartSec=10
StandardOutput=append:$LOG_PATH/logic.log
StandardError=append:$LOG_PATH/logic.log

[Install]
WantedBy=multi-user.target
SERVICE

echo "✅ Systemd services created"
echo ""

# Reload systemd
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable services
echo "Enabling workers to start on boot..."
sudo systemctl enable aicore-language aicore-memory aicore-logic

echo ""
echo "========================================================================"
echo "✅ BASE STATION DEPLOYMENT COMPLETE"
echo "========================================================================"
echo ""
echo "Workers configured:"
echo "  - Language Worker (language_001)"
echo "  - Memory Worker (memory_001)"
echo "  - Logic Worker (logic_001)"
echo ""
echo "To start workers:"
echo "  sudo systemctl start aicore-language"
echo "  sudo systemctl start aicore-memory"
echo "  sudo systemctl start aicore-logic"
echo ""
echo "To check status:"
echo "  sudo systemctl status aicore-language"
echo "  sudo systemctl status aicore-memory"
echo "  sudo systemctl status aicore-logic"
echo ""
echo "To view logs:"
echo "  tail -f $LOG_PATH/language.log"
echo "  tail -f $LOG_PATH/memory.log"
echo "  tail -f $LOG_PATH/logic.log"
echo ""
echo "Workers will auto-start on reboot."
echo ""
