from datetime import date, datetime

from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager)

from django.db import models
from django.utils.translation import gettext as _

from cinema.models import time_to_string


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    birthday = models.DateField(default=date.today().replace(month=1, day=1))
    number = models.IntegerField(default=0)
    promotional_money = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    card = models.IntegerField(default=1111_1111_1111_1111)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def get_birthday_to_date(self) -> str:
        return self.birthday.strftime("%Y-%m-%d")

    @property
    def time_to_string(self) -> str:
        return time_to_string(self.birthday, hours=False)
