from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from knox.auth import TokenAuthentication


class CheckTokenView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request) -> Response:
        return Response({"message": "true", "status": status.HTTP_200_OK})
