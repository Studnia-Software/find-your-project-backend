import datetime
from unittest import TestCase
from knox.models import AuthToken
from rest_framework import status

from ..models import User

import string
import random

from django.contrib.auth.signals import user_logged_in

from datetime import timedelta

from freezegun import freeze_time
from django.utils.timezone import get_default_timezone

from rest_framework.test import APIClient


class FeatureTest(TestCase):
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

    def _login_user(self, user: User, ttl: timedelta = timedelta(minutes=10)) -> (AuthToken, str):
        instance, token = AuthToken.objects.create(user, ttl)
        user_logged_in.send(sender=user.__class__, user=user)
        return instance, token

    def setUp(self):
        self.user = self._create_mock_user(password="Dupa1234")
        self.client = APIClient()

    def test_token_expiry(self):
        initial_datetime = datetime.datetime(2024, 3, 3, 12, 0, 0, tzinfo=get_default_timezone())
        datetime_plus10 = initial_datetime + timedelta(minutes=10, seconds=10)
        with freeze_time(initial_datetime) as frozen_datetime:
            instance, token = self._login_user(user=self.user, ttl=timedelta(minutes=10))
            response = self.client.get(f"/users/check-auth/", HTTP_AUTHORIZATION=f"Token {token}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            frozen_datetime.move_to(datetime_plus10)

            response = self.client.get(f"/users/check-auth/", HTTP_AUTHORIZATION=f"Token {token}")
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

            token_queryset = AuthToken.objects.filter(token_key=token[8:])
            self.assertFalse(token_queryset.exists())
