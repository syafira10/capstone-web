import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import SensorData
from .serializers import SensorDataSerializer


class MonitoringConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time monitoring data"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.group_name = 'monitoring'
        
        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        print(f"WebSocket connected: {self.channel_name}")
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected: {self.channel_name}")
    
    async def receive(self, text_data):
        """Receive message from WebSocket"""
        try:
            data = json.loads(text_data)
            
            # Echo back or process command
            if data.get('type') == 'subscribe':
                await self.send(text_data=json.dumps({
                    'type': 'subscription_confirmed',
                    'message': 'Subscribed to monitoring stream'
                }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
    
    async def mqtt_message(self, event):
        """Handle MQTT message from group"""
        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'type': 'mqtt_update',
            'data': event['message']
        }))
    
    async def broadcast_sensor_data(self, event):
        """Broadcast sensor data to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'sensor_data',
            'data': event['data']
        }))
