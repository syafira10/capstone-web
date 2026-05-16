import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


def get_logger(name):
    """Get a configured logger instance"""
    return logging.getLogger(name)


def format_sensor_topic(topic):
    """Format sensor topic name for display"""
    topic_map = {
        'RAINSENSOR': 'Rain Sensor',
        'WATERLEVELSENSORKAI': 'Water Level - KAI',
        'WATERLEVELSENSORKRL': 'Water Level - KRL',
    }
    return topic_map.get(topic, topic)


def get_status_from_value(topic, value, thresholds=None):
    """Determine status based on topic and value"""
    if thresholds is None:
        thresholds = {
            'WATERLEVELSENSORKAI': {'warning': 60, 'critical': 70},
            'WATERLEVELSENSORKRL': {'warning': 60, 'critical': 70},
        }
    
    if topic in thresholds:
        threshold = thresholds[topic]
        if value >= threshold.get('critical', 100):
            return 'CRITICAL'
        elif value >= threshold.get('warning', 50):
            return 'WARNING'
    
    return 'SAFE'
