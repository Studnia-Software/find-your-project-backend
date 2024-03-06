from unittest import TestCase

from ..models import User
from ..services import UserService
from ..serializers import UserSerializer


class TestUserService(TestCase):
    def setUp(self):
        self.service = UserService()

    def test_create_user(self):
        mock_data = {
            'first_name': 'user2',
            'last_name': 'useruser',
            'email': 'user@userski.com',
            'password': 'Dupa1234'
        }

        serializer = UserSerializer(data=mock_data)
        serializer.is_valid(raise_exception=True)
        instance = self.service.create_user(serializer.validated_data)

        db_instance = User.objects.get(id=instance.id)

        self.assertEqual(instance, db_instance)

    def test_login_with_valid_data(self):
        self.existing_user_data = {
            'first_name': 'Aaaaaa',
            'last_name': 'Bbbbbb',
            'email': 'dupa@dupa.com',
            'password': 'Dupa1234'
        }

        self.user = User.objects.create_user(**self.existing_user_data)

        token = self.service.login(self.existing_user_data['email'], self.existing_user_data['password'])

        print(token)
