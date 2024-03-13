import json
from unittest import TestCase

from django.contrib.auth.signals import user_logged_in, user_logged_out

from rest_framework import status
from rest_framework.test import APIClient

from knox.models import AuthToken
from knox.settings import knox_settings

from .. models import User
import json


class EndpointTests(TestCase):
    def setUp(self):
        self.apiClient = APIClient()

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
        mock_mail = "grzyb@grzyb.grzyb"
        mock_password = "Dupa1234"

        user = User.objects.create_user(
            first_name="Grzyb",
            last_name="Grzybiarz",
            email=mock_mail,
        )
        user.set_password(mock_password)
        user.save()

        response = self.apiClient.post('/users/login/', {'email': mock_mail, 'password': mock_password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(AuthToken.objects.get(user=user).token_key, json.loads(response.content)['token'])

    def test_login_endpoint_with_invalid_data(self):
        response = self.apiClient.post('/users/login/', {'email': 'bademail@chuj.com', 'password': 'ehehehehehehehehehe'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logout_endpoint_with_valid_token(self):
        user = User.objects.create(
            first_name="Chuj",
            last_name="Fiut",
            email="chuj@fiut.com",
        )
        user.set_password("Dupa1234")
        user.save()

        token_ttl = knox_settings.TOKEN_TTL
        instance, token = AuthToken.objects.create(user, token_ttl)
        user_logged_in.send(sender=user.__class__, user=user)

        response = self.apiClient.post('/users/logout/', HTTP_AUTHORIZATION=f'Token {token}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        token_obj = AuthToken.objects.filter(token_key=instance.token_key)
        self.assertEqual(token_obj.exists(), False)

    def test_logout_endpoint_with_invalid_token(self):
        response = self.apiClient.post('/users/logout/', HTTP_AUTHORIZATION=f'Token aaasdasa')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_endpoint_with_no_token(self):
        response = self.apiClient.post('/users/logout/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_logout_all(self):
        pass



