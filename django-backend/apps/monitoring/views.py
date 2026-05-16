from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db.models import Max, Min
from .models import SensorData, Alert, SystemSetting
from .serializers import SensorDataSerializer, AlertSerializer, SystemSettingSerializer


class SensorDataViewSet(viewsets.ModelViewSet):
    """ViewSet for SensorData"""
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer
    
    @action(detail=False, methods=['get'])
    def realtime(self, request):
        """Get latest value for each topic"""
        try:
            data = {}
            for topic_choice, topic_label in SensorData._meta.get_field('topic').choices:
                latest = SensorData.objects.filter(topic=topic_choice).latest('timestamp')
                data[topic_choice] = SensorDataSerializer(latest).data
            return Response({
                'latest': data,
                'timestamp': timezone.now().isoformat()
            })
        except SensorData.DoesNotExist:
            return Response({'latest': {}, 'timestamp': timezone.now().isoformat()})
    
    @action(detail=False, methods=['get'])
    def historical(self, request):
        """Get historical data with optional filters"""
        date_from = request.query_params.get('dateFrom')
        date_to = request.query_params.get('dateTo')
        location = request.query_params.get('location')
        topic = request.query_params.get('topic')
        
        queryset = SensorData.objects.all()
        
        if date_from:
            try:
                queryset = queryset.filter(timestamp__gte=date_from)
            except:
                pass
        
        if date_to:
            try:
                queryset = queryset.filter(timestamp__lte=date_to)
            except:
                pass
        
        if location:
            queryset = queryset.filter(location=location)
        
        if topic:
            queryset = queryset.filter(topic=topic)
        
        # Limit to last 100 entries if no specific date range
        if not date_from and not date_to:
            queryset = queryset[:100]
        
        serializer = SensorDataSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest data for all topics"""
        try:
            topics = ['RAINSENSOR', 'WATERLEVELSENSORKAI', 'WATERLEVELSENSORKRL']
            data = {}
            for topic in topics:
                try:
                    latest = SensorData.objects.filter(topic=topic).latest('timestamp')
                    data[topic] = {
                        'value': latest.value,
                        'timestamp': latest.timestamp.isoformat(),
                        'location': latest.location
                    }
                except SensorData.DoesNotExist:
                    data[topic] = None
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AlertViewSet(viewsets.ModelViewSet):
    """ViewSet for Alerts"""
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active (unacknowledged) alerts"""
        alerts = Alert.objects.filter(acknowledged=False).order_by('-timestamp')
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Acknowledge an alert"""
        alert = self.get_object()
        alert.acknowledged = True
        alert.acknowledged_at = timezone.now()
        alert.save()
        return Response(AlertSerializer(alert).data)


class SystemSettingViewSet(viewsets.ModelViewSet):
    """ViewSet for System Settings"""
    queryset = SystemSetting.objects.all()
    serializer_class = SystemSettingSerializer
    lookup_field = 'key'
    
    @action(detail=False, methods=['get'])
    def thresholds(self, request):
        """Get alert thresholds"""
        try:
            threshold_krl = SystemSetting.objects.get(key='THRESHOLD_WATER_KRL')
            threshold_kai = SystemSetting.objects.get(key='THRESHOLD_WATER_KAI')
            threshold_rain = SystemSetting.objects.get(key='THRESHOLD_RAIN')
            
            return Response({
                'water_krl': float(threshold_krl.value),
                'water_kai': float(threshold_kai.value),
                'rain': float(threshold_rain.value)
            })
        except SystemSetting.DoesNotExist:
            # Return defaults
            return Response({
                'water_krl': 60,
                'water_kai': 70,
                'rain': 50
            })
