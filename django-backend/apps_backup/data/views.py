from rest_framework.views import APIView
from rest_framework.response import Response

class HistoricalDataView(APIView):
    def get(self, request):
        # Return mock historical data
        return Response({"data": []})
