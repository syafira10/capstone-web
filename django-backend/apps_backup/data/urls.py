from django.urls import path
from .views import HistoricalDataView

urlpatterns = [
    path('history/', HistoricalDataView.as_view()),
]
