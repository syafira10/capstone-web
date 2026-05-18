from rest_framework.views import APIView
from rest_framework.response import Response

class NotificationView(APIView):
    def get(self, request):
        # Return mock notifications
        return Response({"notifications": []})
