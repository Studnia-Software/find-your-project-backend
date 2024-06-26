from knox.settings import knox_settings
from knox.models import AuthToken

from rest_framework import exceptions as rest_exceptions
from django.contrib.auth.signals import user_logged_in, user_logged_out

from users.dtos import UserDTO
from users.models import User

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserService:
    def __init__(self, password_reset_token_generator: PasswordResetTokenGenerator = PasswordResetTokenGenerator()):
        self.password_reset_token_generator = password_reset_token_generator

    def _login_user(self, user: User) -> str:
        token_ttl = knox_settings.TOKEN_TTL
        instance, token = AuthToken.objects.create(user, token_ttl)
        user_logged_in.send(sender=user.__class__, user=user)
        return token

    def _get_user_by_email(self, email) -> User:
        return User.objects.filter(email=email).first()

    def create_user(self, user_dto: UserDTO) -> (str, User) or None:
        user = User(
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            email=user_dto.email,
        )

        if user_dto.password is not None:
            user.set_password(user_dto.password)

        user.save()

        token = self._login_user(user)
        return token, user

    def login(self, email: str, password: str) -> (AuthToken, User):
        user = self._get_user_by_email(email)

        if not user.check_password(password):
            raise rest_exceptions.AuthenticationFailed("Wrong password")

        token = self._login_user(user)
        return token, user

    def logout(self, token) -> bool:
        token_instance = AuthToken.objects.filter(token_key=token[:8])

        if not token_instance.exists():
            return False

        token_instance = token_instance[0]
        user_logged_out.send(sender=token_instance.user.__class__, user=token_instance.user)
        token_instance.delete()
        return True

    def logout_all(self, token) -> bool:
        tokens = AuthToken.objects.filter(token_key=token[:8])

        if not tokens.exists():
            return False

        user = AuthToken.objects.get(token_key=token[:8]).user
        AuthToken.objects.filter(user=user).delete()
        return True

    def request_password_reset_token(self, email: str) -> str:
        user = self._get_user_by_email(email)
        token = self.password_reset_token_generator.make_token(user)
        return token

    def reset_password(self, email: str, token: str, new_password: str) -> User:
        user = self._get_user_by_email(email)
        if not user:
            raise ValueError("No user with such email exists")

        valid = self.password_reset_token_generator.check_token(user, token)
        if not valid:
            raise ValueError("Invalid token")

        user.set_password(new_password)
        user.save()

        return user
