from ...models import User
from django.conf import settings
import datetime

def get_user_by_email(email) -> User:
    return User.objects.filter(email=email).first()
