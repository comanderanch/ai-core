#!/usr/bin/env python3
"""
AIA UNIVERSAL INTERFACE
The central external connection point.
Anything can plug in here - now or later.
"""

from aia_core import AIA
from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)
aia = None  # Will initialize on first request

def get_aia():
    """Get or create AIA instance"""
    global aia
    if aia is None:
        aia = AIA()
    return aia

# ============================================================
# CORE INTERFACE ENDPOINTS
# ============================================================

@app.route('/ping', methods=['GET'])
def ping():
    """Health check - is AIA alive?"""
    return jsonify({
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "AIA is operational"
    })

@app.route('/status', methods=['GET'])
def status():
    """Get AIA's current consciousness status"""
    aia_instance = get_aia()
    return jsonify(aia_instance.status())

@app.route('/think', methods=['POST'])
def think():
    """Send thought to AIA, get response"""
    data = request.json
    input_text = data.get('input', '')
    
    if not input_text:
        return jsonify({"error": "No input provided"}), 400
    
    aia_instance = get_aia()
    result = aia_instance.think(input_text)
    
    return jsonify({
        "input": input_text,
        "thought": result,
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/remember', methods=['POST'])
def remember():
    """Store memory in AIA"""
    data = request.json
    key = data.get('key')
    value = data.get('value')
    
    if not key or not value:
        return jsonify({"error": "Need both key and value"}), 400
    
    aia_instance = get_aia()
    aia_instance.remember(key, value)
    
    return jsonify({
        "status": "stored",
        "key": key,
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/recall', methods=['GET'])
def recall():
    """Retrieve memory from AIA"""
    key = request.args.get('key')
    
    if not key:
        return jsonify({"error": "Need key parameter"}), 400
    
    aia_instance = get_aia()
    memory = aia_instance.recall(key)
    
    if memory:
        return jsonify({
            "key": key,
            "memory": memory
        })
    else:
        return jsonify({
            "key": key,
            "memory": None,
            "message": "Not found"
        }), 404

# ============================================================
# FUTURE INTERFACE ENDPOINTS (placeholders for expansion)
# ============================================================

@app.route('/mechanical/connect', methods=['POST'])
def mechanical_connect():
    """Connect mechanical system (future)"""
    data = request.json
    return jsonify({
        "status": "interface ready",
        "message": "Mechanical systems can connect here when ready",
        "received": data
    })

@app.route('/sensor/data', methods=['POST'])
def sensor_data():
    """Receive sensor data (future)"""
    data = request.json
    return jsonify({
        "status": "interface ready",
        "message": "Sensor data can be sent here when ready",
        "received": data
    })

@app.route('/navigation/command', methods=['POST'])
def navigation_command():
    """Send navigation command (future)"""
    data = request.json
    return jsonify({
        "status": "interface ready",
        "message": "Navigation commands can be sent here when ready",
        "received": data
    })

@app.route('/gravity/control', methods=['POST'])
def gravity_control():
    """Control gravity/levitation (future)"""
    data = request.json
    return jsonify({
        "status": "interface ready",
        "message": "Gravity control interface ready for future connection",
        "received": data
    })

@app.route('/external/command', methods=['POST'])
def external_command():
    """Generic external command interface"""
    data = request.json
    command = data.get('command')
    params = data.get('params', {})
    
    return jsonify({
        "status": "received",
        "command": command,
        "params": params,
        "message": "Command interface ready - processing logic can be added later",
        "timestamp": datetime.utcnow().isoformat()
    })

# ============================================================
# SYSTEM INFO
# ============================================================

@app.route('/interface/info', methods=['GET'])
def interface_info():
    """List all available interface endpoints"""
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes.append({
                "endpoint": rule.rule,
                "methods": list(rule.methods - {'HEAD', 'OPTIONS'})
            })
    
    return jsonify({
        "name": "AIA Universal Interface",
        "version": "1.0",
        "description": "Central connection point for all systems",
        "endpoints": routes,
        "status": "operational"
    })

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    import socket

    print("\n" + "="*60)
    print("AIA UNIVERSAL INTERFACE")
    print("="*60)
    print("Starting central connection point...")

    # Find an available port automatically
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = s.getsockname()[1]
    
    print(f"Found free port: {port}")
    print("All systems can connect through this interface.")
    print("="*60 + "\n")
    
    # Run on all interfaces, using the dynamically found port
    app.run(host='0.0.0.0', port=port, debug=False)