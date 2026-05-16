from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorDataViewSet, AlertViewSet, SystemSettingViewSet

router = DefaultRouter()
router.register(r'data', SensorDataViewSet, basename='sensor-data')
router.register(r'alerts', AlertViewSet, basename='alert')
router.register(r'settings', SystemSettingViewSet, basename='setting')

urlpatterns = [
    path('', include(router.urls)),
    path('realtime/', SensorDataViewSet.as_view({'get': 'realtime'}), name='realtime'),
    path('historical/', SensorDataViewSet.as_view({'get': 'historical'}), name='historical'),
    path('latest/', SensorDataViewSet.as_view({'get': 'latest'}), name='latest'),
]
