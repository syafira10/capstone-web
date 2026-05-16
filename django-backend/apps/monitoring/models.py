from django.db import models
from django.utils import timezone


class SensorData(models.Model):
    """Model to store MQTT sensor data"""
    TOPIC_CHOICES = [
        ('RAINSENSOR', 'Rain Sensor'),
        ('WATERLEVELSENSORKAI', 'Water Level Sensor KAI'),
        ('WATERLEVELSENSORKRL', 'Water Level Sensor KRL'),
    ]
    
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)
    value = models.FloatField()
    location = models.CharField(max_length=100, default='Manggarai')
    timestamp = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Sensor Data'
        verbose_name_plural = 'Sensor Data'
        indexes = [
            models.Index(fields=['topic', '-timestamp']),
            models.Index(fields=['location', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.topic} - {self.value} @ {self.timestamp}"


class Alert(models.Model):
    """Model to store system alerts"""
    SEVERITY_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ]
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    location = models.CharField(max_length=100, default='Manggarai')
    timestamp = models.DateTimeField(default=timezone.now)
    acknowledged = models.BooleanField(default=False)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'
    
    def __str__(self):
        return f"[{self.severity.upper()}] {self.title}"


class SystemSetting(models.Model):
    """Model to store system settings"""
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    description = models.CharField(max_length=500, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'System Setting'
        verbose_name_plural = 'System Settings'
    
    def __str__(self):
        return f"{self.key} = {self.value}"
