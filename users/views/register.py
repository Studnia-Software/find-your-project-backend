from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers import UserSerializer
from ..services import UserService

from django.db import IntegrityError


class RegisterView(APIView):
    authentication_classes = [TokenAuthentication]
    user_service = UserService()

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token, user = self.user_service.create_user(serializer.validated_data)
            return Response({"token": token}, status=status.HTTP_201_CREATED)
        except IntegrityError as integrity_error:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": str(integrity_error)})
