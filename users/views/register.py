from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from users.serializers import UserSerializer
from users.services import UserService


class RegisterView(APIView):
    authentication_classes = [TokenAuthentication]

    user_service: UserService = None

    def __init__(self, user_service: UserService, **kwargs):
        super().__init__(**kwargs)
        self.user_service = user_service

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            token, user = self.user_service.create_user(serializer.validated_data)
            return Response({"token": token}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as validation_error:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": str(validation_error)})
