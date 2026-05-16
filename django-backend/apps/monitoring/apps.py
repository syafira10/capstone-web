from django.apps import AppConfig


class MonitoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.monitoring'
    
    def ready(self):
        """Initialize MQTT client when app is ready"""
        try:
            from .services.mqtt_client import mqtt_client
            mqtt_client.start()
            print("[OK] MQTT Client started successfully")
        except Exception as e:
            print(f"[ERROR] Failed to start MQTT Client: {e}")
