from django.urls import path

from .views import (
    latest_data,
    history_data,
    dashboard
)

urlpatterns = [

    path(
        '',
        dashboard
    ),

    path(
        'latest/',
        latest_data
    ),

    path(
        'history/',
        history_data
    ),
]