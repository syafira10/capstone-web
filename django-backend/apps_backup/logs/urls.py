from django.urls import path
from .views import ActivityLogView, ErrorLogView

urlpatterns = [
    path('activity/', ActivityLogView.as_view()),
    path('error/', ErrorLogView.as_view()),
]
