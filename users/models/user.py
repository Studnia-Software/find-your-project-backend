from django.contrib.auth.models import AbstractUser
from .user_details import UserDetails
from django.db.models import OneToOneField, SET_NULL, EmailField
from ..managers.user_manager import UserManager


class User(AbstractUser):
    email = EmailField(unique=True, verbose_name="Email", max_length=255)
    user_details_id = OneToOneField(to=UserDetails, on_delete=SET_NULL, null=True)
    username = None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
