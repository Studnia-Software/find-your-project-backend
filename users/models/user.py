from django.contrib.auth.models import AbstractUser
from .user_details import UserDetails
from django.db.models import OneToOneField, SET_NULL


class CustomUser(AbstractUser):
    user_details_id = OneToOneField(to=UserDetails, on_delete=SET_NULL, null=True)
