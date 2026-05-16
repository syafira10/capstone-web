from rest_framework import serializers
from .models import SensorData, Alert, SystemSetting


class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ['id', 'topic', 'value', 'location', 'timestamp', 'created_at']
        read_only_fields = ['created_at']


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'title', 'message', 'severity', 'location', 'timestamp', 'acknowledged', 'acknowledged_at']


class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = ['key', 'value', 'description', 'updated_at']
