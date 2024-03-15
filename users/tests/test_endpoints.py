from knox.models import AuthToken

from rest_framework import status
from rest_framework.test import APIClient

from unittest import TestCase
import json

from . import utils


class EndpointTests(TestCase):
    def setUp(self):
        self.apiClient = APIClient()
        self.user, self.password = utils.create_mock_user()

    def test_register_endpoint_with_valid_data(self):
        user_data, password = utils.generate_mock_user_data()
        user_data["password"] = password
        response = self.apiClient.post('/users/register/', user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_endpoint_with_repeated_data(self):
        user_data, password = utils.generate_mock_user_data()
        user_data["password"] = password
        self.apiClient.post('/users/register/', user_data)
        response = self.apiClient.post('/users/register/', user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_endpoint_with_invalid_data(self):
        user_data, password = utils.generate_mock_user_data()

        self.apiClient.post('/users/register/', user_data)
        response = self.apiClient.post('/users/register/', user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_endpoint_with_valid_data(self):
        response = self.apiClient.post('/users/login/', {'email': self.user.email, "password": self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(AuthToken.objects.get(user=self.user).token_key, json.loads(response.content)['token'])

    def test_login_endpoint_with_invalid_data(self):
        response = self.apiClient.post('/users/login/', {'email': 'bademail@chuj.com', 'password': 'ehehehehehehehehehe'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logout_endpoint_with_valid_token(self):
        instance, token = utils.login_mock_user(self.user)
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
            utils.login_mock_user(self.user)
        instance, token = utils.login_mock_user(self.user)
        response = self.apiClient.post('/users/logoutall/', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_check_auth_endpoint(self):
        instance, token = utils.login_mock_user(self.user)

        response = self.apiClient.get('/users/check-auth/', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_auth_endpoint_with_invalid_token(self):
        response = self.apiClient.get('/users/check-auth/', HTTP_AUTHORIZATION=f'Token asdasd')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_check_auth_endpoint_with_no_token(self):
        response = self.apiClient.get('/users/check-auth/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



