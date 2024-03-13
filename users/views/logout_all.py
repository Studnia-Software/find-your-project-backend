from django.contrib.auth import login
from knox.auth import TokenAuthentication

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from ..services import UserService


class LogoutAllView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        pass