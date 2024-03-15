from unittest import TestCase
from knox.models import AuthToken

from users.models import User
from users.services import UserService
from users.serializers import UserSerializer
from . import utils

class TestUserService(TestCase):
    def setUp(self):
        self.service = UserService()
        self.user, self.password = utils.create_mock_user()

    def test_create_user(self):
        mock_data, password = utils.generate_mock_user_data()
        mock_data["password"] = password

        serializer = UserSerializer(data=mock_data)
        serializer.is_valid(raise_exception=True)
        token, user = self.service.create_user(serializer.validated_data)

        user_instance = User.objects.get(id=user.id)
        self.assertEqual(user, user_instance)

        token_instance = AuthToken.objects.get(user=user)
        self.assertIn(token_instance.token_key, token)

    def test_login_with_valid_data(self):
        token, user = self.service.login(self.user.email, self.password)
        token_instance = AuthToken.objects.get(user=self.user)

        self.assertIn(token_instance.token_key, token)

    def test_logout_with_valid_token(self):
        instance, token = utils.login_mock_user(user=self.user)
        self.service.logout(token)

        token_instance = AuthToken.objects.filter(token_key=utils.extract_token_key(token))
        self.assertFalse(token_instance.exists())

    def test_logout_with_invalid_token(self):
        logged_out = self.service.logout("asdkljaskdjajs")
        self.assertFalse(logged_out)

    def test_logoutall_with_valid_token(self):
        for i in range(10):
            utils.login_mock_user(user=self.user)
        instance, token = utils.login_mock_user(user=self.user)
        self.service.logout_all(token)
        tokens = AuthToken.objects.filter(user=self.user)
        self.assertFalse(tokens.exists())

    def test_logoutall_with_invalid_token(self):
        logged_out = self.service.logout_all("aaaaaaaaaaaaaaaaaaaaaa")
        self.assertFalse(logged_out)

