from django.contrib.auth import login
from knox.auth import TokenAuthentication

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from ..services import UserService


class LogoutAllView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    user_service = UserService()

    def post(self, request):
        token = request.headers.get('Authorization').split(" ")[1]
        logged_out = self.user_service.logout_all(token)

        if logged_out:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"token": "invalid_token"}, status=status.HTTP_400_BAD_REQUEST)
