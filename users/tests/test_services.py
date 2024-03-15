from unittest import TestCase
from knox.models import AuthToken

from ..models import User
from ..services import UserService
from ..serializers import UserSerializer

import string
import random

from knox.settings import knox_settings
from django.contrib.auth.signals import user_logged_in

class TestUserService(TestCase):
    def _random_str(self, length: int) -> str:
        source = string.ascii_lowercase
        result = ""
        for i in range(length):
            result += random.choice(source)

        return result

    def _create_mock_user(self, password: str) -> User:
        mock_data = {
            'first_name': self._random_str(10),
            'last_name': self._random_str(10),
            'email': f"{self._random_str(10)}@grzybowski.com",
        }

        user = User.objects.create_user(**mock_data)

        user.set_password(password)
        user.save()

        return user

    def _login_user(self, user) -> (AuthToken, str):
        token_ttl = knox_settings.TOKEN_TTL
        instance, token = AuthToken.objects.create(user, token_ttl)
        user_logged_in.send(sender=user.__class__, user=user)
        return instance, token

    def setUp(self):
        self.service = UserService()
        self.user = self._create_mock_user(password="Dupa1234")

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
        token, user = self.service.login(self.user.email, "Dupa1234")
        token_instance = AuthToken.objects.get(user=self.user)

        self.assertIn(token_instance.token_key, token)

    def test_logout_with_valid_token(self):
        self.user = self._create_mock_user(password="Dupa1234")
        instance, token = self._login_user(user=self.user)
        self.service.logout(token)

        token_instance = AuthToken.objects.filter(token_key=token[:8])
        self.assertFalse(token_instance.exists())

    def test_logout_with_invalid_token(self):
        logged_out = self.service.logout("asdkljaskdjajs")
        self.assertFalse(logged_out)

    def test_logoutall_with_valid_token(self):
        for i in range(10):
            self._login_user(user=self.user)
        instance, token = self._login_user(user=self.user)
        self.service.logout_all(token)
        tokens = AuthToken.objects.filter(user=self.user)
        self.assertFalse(tokens.exists())

    def test_logoutall_with_invalid_token(self):
        logged_out = self.service.logout_all("aaaaaaaaaaaaaaaaaaaaaa")
        self.assertFalse(logged_out)

