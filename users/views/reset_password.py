from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.services import UserService


class ResetPasswordView(APIView):
    user_service = None

    def __init__(self, user_service: UserService):
        super().__init__()
        self.user_service = user_service

    def post(self, request, *args, **kwargs) -> Response:
        # move into serializer
        email = request.data.get('email')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        #

        try:
            self.user_service.reset_password(email, token, new_password)
            return Response("success", status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

