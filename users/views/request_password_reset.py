from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.services import UserService
from users.services import EmailService


class RequestPasswordResetView(APIView):
    user_service = None

    def __init__(self, user_service: UserService):
        super().__init__()
        self.user_service = user_service
        self.email_service = EmailService()

    def post(self, request):
        email = request.data.get('email')
        try:
            token = self.user_service.request_password_reset_token(email)
            self.email_service.send_email(token, "recovery", email)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
