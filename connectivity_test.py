#!/usr/bin/env python
"""
Connectivity Test Script untuk flood monitoring system
Tests: MQTT Broker → Django API → Database → WebSocket
"""

import os
import sys
import subprocess
import time
import socket
import requests
import json

# Add django backend to path
sys.path.insert(0, 'C:\\Users\\User\\OneDrive\\Documents\\capstone\\system\\django-backend')

print("=" * 70)
print("FLOOD MONITORING SYSTEM - CONNECTIVITY TEST")
print("=" * 70)

# Test 1: Check if backend is running
print("\n[TEST 1] Backend Server Status (Port 8000)")
print("-" * 70)
try:
    response = requests.get('http://localhost:8000/api/monitoring/latest/', timeout=2)
    if response.status_code == 200:
        print("✓ Django backend is responding on port 8000")
        print(f"  Response time: {response.elapsed.total_seconds():.3f}s")
        data = response.json()
        print(f"  Data received: {json.dumps(data, indent=2)[:200]}...")
    else:
        print(f"✗ Backend returned status code: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("✗ Cannot connect to Django backend (port 8000)")
    print("  → Make sure Django server is running with: python manage.py runserver 0.0.0.0:8000")
except Exception as e:
    print(f"✗ Error connecting to backend: {e}")

# Test 2: Test REST API Endpoints
print("\n[TEST 2] REST API Endpoints")
print("-" * 70)
endpoints = [
    ("GET", "/api/monitoring/realtime/"),
    ("GET", "/api/monitoring/latest/"),
    ("GET", "/api/monitoring/historical/?limit=5"),
    ("GET", "/api/monitoring/data/"),
    ("GET", "/api/monitoring/alerts/active/"),
]

for method, endpoint in endpoints:
    try:
        url = f"http://localhost:8000{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=2)
        
        if response.status_code == 200:
            print(f"✓ {method:6} {endpoint:40} → 200 OK")
        else:
            print(f"✗ {method:6} {endpoint:40} → {response.status_code}")
    except Exception as e:
        print(f"✗ {method:6} {endpoint:40} → Error: {str(e)[:40]}")

# Test 3: Check Database
print("\n[TEST 3] Database Status")
print("-" * 70)
try:
    os.chdir('C:\\Users\\User\\OneDrive\\Documents\\capstone\\system\\django-backend')
    result = subprocess.run(
        [
            'C:\\Users\\User\\OneDrive\\Documents\\capstone\\system\\django-backend\\venv\\Scripts\\python.exe',
            '-c',
            """
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from apps.monitoring.models import SensorData, Alert
sensor_count = SensorData.objects.count()
alert_count = Alert.objects.count()
print(f'Sensor records: {sensor_count}')
print(f'Alert records: {alert_count}')
"""
        ],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode == 0:
        print("✓ Database is accessible")
        for line in result.stdout.strip().split('\n'):
            print(f"  {line}")
    else:
        print(f"✗ Database error: {result.stderr}")
except Exception as e:
    print(f"✗ Cannot check database: {e}")

# Test 4: Check MQTT Broker Connectivity
print("\n[TEST 4] MQTT Broker Connectivity")
print("-" * 70)
try:
    import paho.mqtt.client as mqtt
    
    # Test basic connection
    client = mqtt.Client(client_id="connectivity-test")
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("✓ MQTT broker connection successful")
            client.disconnect()
        else:
            print(f"✗ MQTT connection failed with code: {rc}")
            print(f"  Error codes: 1=protocol, 2=ID, 3=unavailable, 4=bad auth, 5=not authorized")
    
    def on_disconnect(client, userdata, rc):
        pass
    
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    
    print("  Connecting to broker.emqx.io:1883...")
    client.connect("broker.emqx.io", 1883, 60)
    client.loop_start()
    time.sleep(2)
    client.loop_stop()
    
except ImportError:
    print("✗ paho-mqtt not installed")
except Exception as e:
    print(f"✗ MQTT test failed: {e}")

# Test 5: Check WebSocket
print("\n[TEST 5] WebSocket Connectivity")
print("-" * 70)
print("  Cannot test WebSocket from command line (requires browser)")
print("  To test WebSocket:")
print("  1. Open browser DevTools (F12)")
print("  2. Run in console:")
print("    ws = new WebSocket('ws://localhost:8000/ws/monitoring/')")
print("    ws.onmessage = (e) => console.log(JSON.parse(e.data))")
print("  3. Watch for incoming MQTT messages")

# Test 6: Frontend Connection Test
print("\n[TEST 6] Frontend Configuration")
print("-" * 70)
try:
    with open('C:\\Users\\User\\OneDrive\\Documents\\capstone\\system\\capstone-web\\.env', 'r') as f:
        env_content = f.read()
        print("✓ Frontend .env file found:")
        for line in env_content.strip().split('\n'):
            if line.strip():
                print(f"  {line}")
except FileNotFoundError:
    print("✗ Frontend .env file not found")
except Exception as e:
    print(f"✗ Error reading .env: {e}")

# Test 7: Network Port Status
print("\n[TEST 7] Network Ports Status")
print("-" * 70)
ports = {
    8000: "Django Backend",
    5173: "Frontend (Vite)",
    5174: "Frontend (Vite alt)",
    1883: "MQTT Broker (external)",
}

for port, service in ports.items():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            print(f"✓ Port {port:5} ({service:30}) - OPEN")
        else:
            if port in [8000, 5173]:
                print(f"✗ Port {port:5} ({service:30}) - CLOSED (should be open)")
            else:
                print(f"⊘ Port {port:5} ({service:30}) - CLOSED (expected if not running)")
    except Exception as e:
        print(f"⊘ Port {port:5} ({service:30}) - Cannot check: {e}")

# Summary
print("\n" + "=" * 70)
print("CONNECTIVITY TEST SUMMARY")
print("=" * 70)
print("""
Data Flow Path:
  IoT Sensors → MQTT Broker (broker.emqx.io:1883)
         ↓
  Django MQTT Client (mqtt_client.py)
         ↓
  SQLite Database (db.sqlite3)
         ↓
  Django REST API (/api/monitoring/*)
         ↓
  React Frontend (localhost:5173/5174)
         ↓
  WebSocket Updates (ws://localhost:8000/ws/monitoring/)

✓ = Working correctly
✗ = Error/Issue found
⊘ = Expected behavior (not running or not required)
""")
print("=" * 70)
