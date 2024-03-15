import string
import random
from unittest import TestCase

from django.contrib.auth.signals import user_logged_in, user_logged_out

from rest_framework import status
from rest_framework.test import APIClient

from knox.models import AuthToken
from knox.settings import knox_settings

from .. models import User
import json


class EndpointTests(TestCase):
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
        self.apiClient = APIClient()
        self.user = self._create_mock_user(password="Dupa1234")

    def test_register_endpoint_with_valid_data(self):
        mock_data = {
            'first_name': 'Grzyb',
            'last_name': 'Grzybowski',
            'email': 'grzyb@grzybowski.com',
            'password': 'Dupa1234'
        }

        response = self.apiClient.post('/users/register/', mock_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_endpoint_with_repeated_data(self):
        mock_data = {
            'first_name': 'Grzyb1',
            'last_name': 'Grzybowski',
            'email': 'grzyb1@grzybowski.com',
            'password': 'Dupa1234'
        }

        self.apiClient.post('/users/register/', mock_data)
        response = self.apiClient.post('/users/register/', mock_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_endpoint_with_invalid_data(self):
        mock_data = {
            'last_name': 'Grzybowski',
            'password': 'Dupa1234'
        }

        self.apiClient.post('/users/register/', mock_data)
        response = self.apiClient.post('/users/register/', mock_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_endpoint_with_valid_data(self):
        response = self.apiClient.post('/users/login/', {'email': self.user.email, 'password': "Dupa1234"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(AuthToken.objects.get(user=self.user).token_key, json.loads(response.content)['token'])

    def test_login_endpoint_with_invalid_data(self):
        response = self.apiClient.post('/users/login/', {'email': 'bademail@chuj.com', 'password': 'ehehehehehehehehehe'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logout_endpoint_with_valid_token(self):
        instance, token = self._login_user(self.user)
        self.apiClient.post('/users/logout/', HTTP_AUTHORIZATION=f'Token {token}')
        token_obj = AuthToken.objects.filter(token_key=instance.token_key)
        self.assertEqual(token_obj.exists(), False)

    def test_logout_endpoint_with_invalid_token(self):
        response = self.apiClient.post('/users/logout/', HTTP_AUTHORIZATION=f'Token aaasdasa')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_endpoint_with_no_token(self):
        response = self.apiClient.post('/users/logout/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_all_endpoint(self):
        for i in range(3):
            self._login_user(self.user)
        instance, token = self._login_user(self.user)
        response = self.apiClient.post('/users/logoutall/', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_check_auth_endpoint(self):
        instance, token = self._login_user(self.user)

        response = self.apiClient.get('/users/check-auth/', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_auth_endpoint_with_invalid_token(self):
        response = self.apiClient.get('/users/check-auth/', HTTP_AUTHORIZATION=f'Token asdasd')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_check_auth_endpoint_with_no_token(self):
        response = self.apiClient.get('/users/check-auth/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



