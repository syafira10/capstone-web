from django.http import JsonResponse
from django.shortcuts import render

from .models import FloodData


# ======================================
# DASHBOARD PAGE
# ======================================

def dashboard(request):

    return render(
        request,
        'dashboard/index.html'
    )


# ======================================
# LATEST REALTIME DATA
# ======================================

def latest_data(request):

    latest = FloodData.objects.last()

    if latest:

        data = {

            "rain": latest.rain_value,

            "krl_cm": latest.krl_water_level,

            "kai_cm": latest.kai_water_level,

            "status": latest.status,

            "timestamp": latest.created_at,
        }

    else:

        data = {

            "message": "No sensor data"
        }

    return JsonResponse(data)


# ======================================
# HISTORY DATA
# ======================================

def history_data(request):

    records = FloodData.objects.all().order_by(
        '-created_at'
    )[:10]

    data = []

    for item in records:

        data.append({

            "rain": item.rain_value,

            "krl_cm": item.krl_water_level,

            "kai_cm": item.kai_water_level,

            "status": item.status,

            "timestamp": item.created_at,
        })

    return JsonResponse(
        data,
        safe=False
    )