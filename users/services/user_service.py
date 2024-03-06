from ..dtos import UserDTO
from ..models import User
from . import helpers
from rest_framework import exceptions


class UserService:
    def create_user(self, user_dto: UserDTO) -> User or None:
        instance = User(
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            email=user_dto.email,
        )

        if user_dto.password is not None:
            instance.set_password(user_dto.password)

        instance.save()
        return instance

    def login(self, email: str, password: str) -> str:
        user = helpers.get_user_by_email(email)

        if user is None:
            raise exceptions.AuthenticationFailed("No user with such email exists")

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Wrong password")

        token = helpers.create_token(user.id)
        return token
