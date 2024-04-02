from django.contrib.auth import login
from knox.auth import TokenAuthentication

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from users.services import UserService
from users.views.utils import get_auth_token


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    user_service: UserService = None

    def __init__(self, user_service: UserService, **kwargs):
        super().__init__(**kwargs)
        self.user_service = user_service

    def post(self, request):
        token = get_auth_token(request)

        logged_out = self.user_service.logout(token)
        if logged_out:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"token": "invalid_token"}, status=status.HTTP_400_BAD_REQUEST)
