from rest_framework.views import APIView
from rest_framework.response import Response

class MonitoringView(APIView):
    def get(self, request):
        # Return mock monitoring data
        return Response({"stations": []})
