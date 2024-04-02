import datetime

from knox.models import AuthToken
from knox.settings import knox_settings

from django.contrib.auth.signals import user_logged_in

import string
import random

from .. models import User


def random_str(length: int, source: str = string.ascii_lowercase) -> str:
    return "".join(random.choice(source) for _ in range(length))


def generate_mock_user_data() -> (dict, str):
    mock_data = {
        'first_name': random_str(10),
        'last_name': random_str(10),
        'email': f"{random_str(10)}@grzybowski.com",
    }
    mock_password = random_str(16)
    return mock_data, mock_password


def create_mock_user() -> (User, str):
    user_data, password = generate_mock_user_data()
    user = User.objects.create_user(**user_data)
    user.set_password(password)
    user.save()
    return user, password


def login_mock_user(user: User, token_ttl: datetime.timedelta = knox_settings.TOKEN_TTL) -> (AuthToken, str):
    instance, token = AuthToken.objects.create(user, token_ttl)
    user_logged_in.send(sender=user.__class__, user=user)
    return instance, token


def extract_token_key(token: str) -> str:
    return token[:8]
