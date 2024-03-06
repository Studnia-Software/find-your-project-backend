import sys

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers import UserSerializer
from ..services import UserService

from django.db import IntegrityError


class LoginView(APIView):
    user_service = UserService()

    def post(self, request):
        jwt_token = self.user_service.login(request.data['email'], request.data['password'])
        response = Response()
        response.set_cookie('jwt', jwt_token)
        response.status_code = status.HTTP_200_OK
        return response
