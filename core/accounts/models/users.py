from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extera_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extera_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extera_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        extera_fields.setdefault("is_staff", True)
        extera_fields.setdefault("is_superuser", True)
        extera_fields.setdefault("is_active", True)
        extera_fields.setdefault("is_verified", True)

        if extera_fields.get("is_staff") is not True:
            raise ValueError("staff user most be not True")

        if extera_fields.get("is_superuser") is not True:
            raise ValueError("super user most be not True")
        self.create_user(email, password, **extera_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=255,
        verbose_name="username",
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()
