from unittest import TestCase
from knox.models import AuthToken

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
        token, user = self.service.create_user(serializer.validated_data)

        user_instance = User.objects.get(id=user.id)
        self.assertEqual(user, user_instance)

        token_instance = AuthToken.objects.get(user=user)
        self.assertIn(token_instance.token_key, token)

    def test_login_with_valid_data(self):
        self.existing_user_data = {
            'first_name': 'Aaaaaa',
            'last_name': 'Bbbbbb',
            'email': 'dupa@dupa.com',
            'password': 'Dupa1234'
        }

        self.user = User.objects.create_user(**self.existing_user_data)

        token, user = self.service.login(self.existing_user_data['email'], self.existing_user_data['password'])
        token_instance = AuthToken.objects.get(user=self.user)

        self.assertIn(token_instance.token_key, token)

    def test_logout_with_valid_token(self):
        self.existing_user_data = {
            'first_name': 'Aaaaaa',
            'last_name': 'Bbbbbb',
            'email': 'dupa@chuj.com',
            'password': 'Dupa1234'
        }

        self.user = User.objects.create_user(**self.existing_user_data)
        token, user = self.service.login(self.existing_user_data['email'], self.existing_user_data['password'])

        logged_out = self.service.logout(token)
        self.assertTrue(logged_out)

        token_instance = AuthToken.objects.filter(token_key=token[:8])
        self.assertFalse(token_instance.exists())

    def test_logout_with_invalid_token(self):
        logged_out = self.service.logout("asdkljaskdjajs")
        self.assertFalse(logged_out)

