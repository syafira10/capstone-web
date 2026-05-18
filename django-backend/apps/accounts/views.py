from rest_framework.views import APIView
from rest_framework.response import Response

class LoginView(APIView):
    def post(self, request):
        # Implement login logic
        return Response({"token": "mock-token"})
