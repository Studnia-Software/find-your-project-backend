import json
from unittest import TestCase

from rest_framework import status
from rest_framework.test import APIClient


class EndpointTests(TestCase):
    def setUp(self):
        self.apiClient = APIClient()

    def test_register_endpoint(self):
        mock_data = {
            'first_name': 'Grzyb',
            'last_name': 'Grzybowski',
            'email': 'grzyb@grzybowski.com',
            'password': 'Dupa1234'
        }
        response = self.apiClient.post('/users/register/', mock_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

