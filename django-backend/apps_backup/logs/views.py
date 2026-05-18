from rest_framework.views import APIView
from rest_framework.response import Response

class ActivityLogView(APIView):
    def get(self, request):
        # Return mock activity logs
        return Response({"activity_logs": []})

class ErrorLogView(APIView):
    def get(self, request):
        # Return mock error logs
        return Response({"error_logs": []})
