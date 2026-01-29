#!/bin/bash
# Start all background services for AI-Core

echo "Starting AI-Core background services..."

# AIA Universal Interface (port 5000)
nohup python3 aia_interface.py > logs/aia_interface.log 2>&1 &
echo "✅ AIA Interface started (PID $!)"

# Add other background services here as needed
# Example:
# nohup python3 scripts/some_background_script.py > logs/background.log 2>&1 &

echo "All background services started."
echo "Check logs/ directory to monitor them."
echo ""
echo "To stop services:"
echo "  pkill -f aia_interface"
