from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from users.services import UserService
from users.services import EmailService
from users.serializers import EmailSerializer


class RequestPasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    user_service: UserService = None
    email_service: EmailService = None

    def __init__(self, user_service: UserService, email_service: EmailService, **kwargs):
        super().__init__(**kwargs)
        self.user_service = user_service
        self.email_service = email_service

    def post(self, request):
        email_serializer = EmailSerializer(data={"email": request.data.get('email')})

        try:
            email_serializer.is_valid(raise_exception=True)
            token = self.user_service.request_password_reset_token(email_serializer.data["email"])
            self.email_service.send_email(token, "recovery", email_serializer.data["email"])
            return Response(status=status.HTTP_204_NO_CONTENT)
        except serializers.ValidationError as validation_error:
            return Response({'error': str(validation_error)}, status=status.HTTP_400_BAD_REQUEST)
