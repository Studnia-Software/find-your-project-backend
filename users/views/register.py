from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers import UserSerializer
from ..services import UserService


class RegisterView(APIView):
    user_service = UserService()

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_created = self.user_service.create_user(serializer.validated_data)

        if user_created:
            # return Response(data={"message": "User created"}, status=status.HTTP_201_CREATED)
            pass
        else:
            # return Response(data={"message": "Something broke"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            pass
