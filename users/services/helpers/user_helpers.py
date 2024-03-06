from ...models import User
from django.conf import settings
import datetime
import jwt


def get_user_by_email(email) -> User:
    return User.objects.filter(email=email).first()


def create_token(user_id: int) -> str:
    payload = dict(
        id=user_id,
        exp=datetime.datetime.utcnow() + datetime.timedelta(hours=48),
        iat=datetime.datetime.utcnow()
    )

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return token
