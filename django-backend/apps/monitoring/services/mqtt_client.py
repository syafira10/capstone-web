import paho.mqtt.client as mqtt
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
import json
import threading
import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)


class MQTTClientService:
    """Service to handle MQTT subscriptions and message processing"""
    
    def __init__(self):
        self.client = None
        self.connected = False
        self.latest_values = {}
        self.lock = threading.Lock()
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback for MQTT connection"""
        if rc == 0:
            self.connected = True
            logger.info("✓ MQTT broker connected successfully")
            
            # Subscribe to topics
            for topic in settings.MQTT_TOPICS:
                client.subscribe(topic, qos=1)
                logger.info(f"✓ Subscribed to topic: {topic}")
        else:
            self.connected = False
            logger.error(f"✗ MQTT connection failed with code {rc}")
    
    def on_disconnect(self, client, userdata, rc):
        """Callback for MQTT disconnection"""
        self.connected = False
        if rc != 0:
            logger.warning(f"✗ Unexpected MQTT disconnection with code {rc}")
        else:
            logger.info("✓ MQTT disconnected gracefully")
    
    def on_message(self, client, userdata, msg):
        """Callback for MQTT message received"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8').strip()
            
            # Parse the value
            try:
                value = float(payload)
            except ValueError:
                logger.warning(f"✗ Invalid payload for {topic}: {payload}")
                return
            
            logger.info(f"→ MQTT Message: {topic} = {value}")
            
            # Store latest value in memory
            with self.lock:
                self.latest_values[topic] = {
                    'value': value,
                    'timestamp': timezone.now()
                }
            
            # Save to database
            self._save_sensor_data(topic, value)
            
            # Broadcast to WebSocket clients
            self._broadcast_to_websocket(topic, value)
            
            # Check thresholds and create alerts if needed
            self._check_thresholds_and_alert(topic, value)
            
        except Exception as e:
            logger.error(f"✗ Error processing MQTT message: {e}")
    
    def on_subscribe(self, client, userdata, mid, granted_qos):
        """Callback for subscription"""
        logger.info(f"✓ Subscription acknowledged with QoS: {granted_qos}")
    
    def on_log(self, client, userdata, level, buf):
        """Callback for logging"""
        if level == mqtt.MQTT_LOG_DEBUG:
            logger.debug(f"MQTT: {buf}")
    
    def _save_sensor_data(self, topic, value):
        """Save sensor data to database"""
        try:
            from ..models import SensorData
            
            SensorData.objects.create(
                topic=topic,
                value=value,
                location=settings.MQTT_LOCATION,
                timestamp=timezone.now()
            )
            logger.debug(f"✓ Saved {topic}={value} to database")
        except Exception as e:
            logger.error(f"✗ Failed to save sensor data: {e}")
    
    def _broadcast_to_websocket(self, topic, value):
        """Broadcast message to WebSocket consumers"""
        try:
            channel_layer = get_channel_layer()
            message = {
                'type': 'mqtt_message',
                'message': {
                    'topic': topic,
                    'value': value,
                    'timestamp': timezone.now().isoformat(),
                    'location': settings.MQTT_LOCATION
                }
            }
            
            # Send to monitoring group
            async_to_sync(channel_layer.group_send)(
                'monitoring',
                {
                    'type': 'mqtt_message',
                    'message': message['message']
                }
            )
            logger.debug(f"✓ Broadcasted {topic}={value} to WebSocket")
        except Exception as e:
            logger.debug(f"⊘ WebSocket broadcast skipped (might not be connected): {e}")
    
    def _check_thresholds_and_alert(self, topic, value):
        """Check thresholds and create alerts if necessary"""
        try:
            from ..models import Alert
            
            alert_created = False
            alert_message = None
            severity = None
            
            if topic in ['WATERLEVELSENSORKAI', 'WATERLEVELSENSORKRL']:
                # Water level alerts
                if value >= settings.WATER_LEVEL_THRESHOLD_CRITICAL:
                    severity = 'critical'
                    alert_message = f"CRITICAL: {topic} water level reached {value} cm"
                    alert_created = True
                elif value >= settings.WATER_LEVEL_THRESHOLD_WARNING:
                    severity = 'warning'
                    alert_message = f"WARNING: {topic} water level reached {value} cm"
                    alert_created = True
            
            elif topic == 'RAINSENSOR':
                # Rain intensity alerts
                if value >= settings.RAIN_INTENSITY_THRESHOLD_WARNING:
                    severity = 'warning'
                    alert_message = f"WARNING: Heavy rain detected - intensity: {value} mm/h"
                    alert_created = True
            
            if alert_created and alert_message:
                # Check if similar alert exists in last 5 minutes
                from django.utils.timezone import timedelta
                recent_alerts = Alert.objects.filter(
                    title=alert_message[:100],
                    timestamp__gte=timezone.now() - timedelta(minutes=5)
                )
                
                if not recent_alerts.exists():
                    Alert.objects.create(
                        title=alert_message[:100],
                        message=alert_message,
                        severity=severity,
                        location=settings.MQTT_LOCATION
                    )
                    logger.info(f"✓ Alert created: {alert_message}")
        
        except Exception as e:
            logger.error(f"✗ Failed to check thresholds: {e}")
    
    def start(self):
        """Start the MQTT client"""
        try:
            self.client = mqtt.Client(client_id=settings.MQTT_CLIENT_ID)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.on_disconnect = self.on_disconnect
            self.client.on_subscribe = self.on_subscribe
            # self.client.on_log = self.on_log  # Uncomment for debugging
            
            logger.info(f"Connecting to MQTT broker at {settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}")
            self.client.connect(
                settings.MQTT_BROKER_HOST,
                settings.MQTT_BROKER_PORT,
                keepalive=60
            )
            
            # Start the client loop in a separate thread
            self.client.loop_start()
            logger.info("✓ MQTT client started in background thread")
            
        except Exception as e:
            logger.error(f"✗ Failed to start MQTT client: {e}")
    
    def stop(self):
        """Stop the MQTT client"""
        try:
            if self.client:
                self.client.loop_stop()
                self.client.disconnect()
                logger.info("✓ MQTT client stopped")
        except Exception as e:
            logger.error(f"✗ Failed to stop MQTT client: {e}")
    
    def get_latest_values(self):
        """Get latest values for all topics"""
        with self.lock:
            return dict(self.latest_values)


# Global MQTT client instance
mqtt_client = MQTTClientService()
