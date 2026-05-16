#!/usr/bin/env python3
"""
Real-Time MQTT Test Publisher
Helps test real-time updates by publishing simulated sensor data
"""

import paho.mqtt.client as mqtt
import time
import random
import sys
from datetime import datetime

# MQTT Configuration
BROKER_HOST = "broker.emqx.io"
BROKER_PORT = 1883
TOPICS = {
    "RAINSENSOR": (0, 100),              # 0-100 mm/h
    "WATERLEVELSENSORKRL": (40, 85),     # 40-85 cm  
    "WATERLEVELSENSORKAI": (40, 85),     # 40-85 cm
}

def on_connect(client, userdata, flags, rc):
    """Callback for MQTT connection"""
    if rc == 0:
        print(f"✓ Connected to MQTT broker at {BROKER_HOST}:{BROKER_PORT}")
    else:
        print(f"✗ Failed to connect with code {rc}")
        sys.exit(1)

def on_disconnect(client, userdata, rc):
    """Callback for MQTT disconnection"""
    if rc != 0:
        print(f"✗ Unexpected MQTT disconnection with code {rc}")

def on_publish(client, userdata, mid):
    """Callback for published message"""
    print(f"  ✓ Message published successfully (mid: {mid})")

def publish_test_message(client, topic, value):
    """Publish a single test message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n📤 Publishing {timestamp}")
    print(f"  Topic:  {topic}")
    print(f"  Value:  {value}")
    
    client.publish(topic, str(value), qos=1)

def run_interactive_mode():
    """Interactive mode - publish messages manually"""
    client = mqtt.Client(client_id="test-publisher-interactive")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    
    print("\n" + "="*60)
    print("MQTT TEST PUBLISHER - INTERACTIVE MODE")
    print("="*60)
    print("\nConnecting to MQTT broker...")
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()
    
    time.sleep(1)  # Wait for connection
    
    print("\n" + "-"*60)
    print("Available Topics:")
    for i, topic in enumerate(TOPICS.keys(), 1):
        min_val, max_val = TOPICS[topic]
        print(f"  {i}. {topic:25} (range: {min_val}-{max_val})")
    print("\nCommands:")
    print("  p <topic_num> <value>  - Publish to topic with value")
    print("  r <topic_num>           - Publish random value to topic")
    print("  s                       - Send sample burst (3 messages)")
    print("  q                       - Quit")
    print("-"*60)
    
    topic_list = list(TOPICS.keys())
    
    while True:
        try:
            cmd = input("\n> ").strip().split()
            
            if not cmd:
                continue
            
            if cmd[0].lower() == 'q':
                print("\nDisconnecting...")
                break
            
            elif cmd[0].lower() == 'p':
                if len(cmd) < 3:
                    print("✗ Usage: p <topic_num> <value>")
                    print("  Example: p 1 45.5")
                    continue
                
                try:
                    topic_idx = int(cmd[1]) - 1
                    value = float(cmd[2])
                    
                    if 0 <= topic_idx < len(topic_list):
                        topic = topic_list[topic_idx]
                        publish_test_message(client, topic, value)
                    else:
                        print(f"✗ Topic number must be 1-{len(topic_list)}")
                except (ValueError, IndexError):
                    print("✗ Invalid topic number or value")
                    print(f"  Example: p 1 45.5")
            
            elif cmd[0].lower() == 'r':
                if len(cmd) < 2:
                    print("✗ Usage: r <topic_num>")
                    continue
                
                try:
                    topic_idx = int(cmd[1]) - 1
                    if 0 <= topic_idx < len(topic_list):
                        topic = topic_list[topic_idx]
                        min_val, max_val = TOPICS[topic]
                        value = random.uniform(min_val, max_val)
                        publish_test_message(client, topic, round(value, 2))
                    else:
                        print(f"✗ Topic number must be 1-{len(topic_list)}")
                except ValueError:
                    print("✗ Invalid topic number")
            
            elif cmd[0].lower() == 's':
                print("\n📤 Sending sample burst...")
                for topic in topic_list:
                    min_val, max_val = TOPICS[topic]
                    value = random.uniform(min_val, max_val)
                    print(f"  {topic}: {round(value, 2)}")
                    client.publish(topic, str(round(value, 2)), qos=1)
                    time.sleep(0.3)
                print("✓ Burst complete")
            
            else:
                print("✗ Unknown command. Use: p, r, s, or q")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
            break
        except Exception as e:
            print(f"✗ Error: {e}")
    
    client.loop_stop()
    client.disconnect()
    print("✓ Disconnected from broker\n")

def run_automated_mode():
    """Automated mode - publish messages at intervals"""
    client = mqtt.Client(client_id="test-publisher-automated")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    
    print("\n" + "="*60)
    print("MQTT TEST PUBLISHER - AUTOMATED MODE")
    print("="*60)
    print(f"\nBroker: {BROKER_HOST}:{BROKER_PORT}")
    print(f"Topics: {', '.join(TOPICS.keys())}")
    print("Interval: 5 seconds\n")
    print("Publishing random data every 5 seconds...")
    print("Press Ctrl+C to stop\n")
    
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()
    
    try:
        message_count = 0
        while True:
            for topic, (min_val, max_val) in TOPICS.items():
                value = random.uniform(min_val, max_val)
                publish_test_message(client, topic, round(value, 2))
                time.sleep(0.5)
            
            message_count += len(TOPICS)
            print(f"\n{'='*60}")
            print(f"Total messages published: {message_count}")
            print(f"Waiting 5 seconds before next batch...")
            print(f"{'='*60}")
            time.sleep(5)
    
    except KeyboardInterrupt:
        print("\n\n✓ Stopped by user")
    
    finally:
        client.loop_stop()
        client.disconnect()
        print("✓ Disconnected from broker\n")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("REAL-TIME MQTT TEST PUBLISHER")
    print("="*60)
    print("\nUsage: python mqtt_test_publisher.py [mode]")
    print("  Modes:")
    print("    interactive  - Publish messages interactively")
    print("    automated    - Auto-publish random data every 5 seconds")
    print("    (default)    - Interactive mode\n")
    
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "interactive"
    
    if mode == "automated":
        run_automated_mode()
    elif mode == "interactive" or mode == "int":
        run_interactive_mode()
    else:
        print(f"✗ Unknown mode: {mode}")
        print("Use: interactive or automated\n")
        sys.exit(1)
