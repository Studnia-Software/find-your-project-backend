from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from users.services import UserService
from users.serializers import LoginSerializer
from rest_framework import serializers


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    user_service: UserService = None

    def __init__(self, user_service: UserService, **kwargs):
        super().__init__(**kwargs)
        self.user_service = user_service

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        try:
            login_serializer.is_valid(raise_exception=True)
            token, user = self.user_service.login(**login_serializer.data)
            return Response({"token": token}, status=status.HTTP_200_OK)
        except serializers.ValidationError as validation_error:
            return Response(data={"detail": str(validation_error)}, status=status.HTTP_401_UNAUTHORIZED)
