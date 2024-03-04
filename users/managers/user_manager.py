from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, first_name: str, last_name: str, email: str, password: str = None, is_staff=False, is_superuser=False, **extra_fields) -> 'User':
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not email:
            raise ValueError("Users must have an email")

        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser

        user.save(using=self._db)
        return user

    def create_superuser(self, first_name: str, last_name: str, email: str, password: str = None) -> 'User':
        superuser = self.create_user(first_name, last_name, email, password, is_staff=True, is_superuser=True)
        superuser.save(using=self._db)
        return superuser