from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from ..services import UserService


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    user_service = UserService()

    def post(self, request):
        token, user = self.user_service.login(request.data['email'], request.data['password'])
        return Response({"token": token}, status=status.HTTP_200_OK)

