import json
from unittest import TestCase

from rest_framework import status
from rest_framework.test import APIClient


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
