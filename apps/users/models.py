from typing import TypeVar
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.models import BaseModel
from apps.users.enums import Gender, UserStatus
from apps.users.managers import UserManager

UserType = TypeVar("UserType", bound="User")


class User(BaseModel, AbstractUser):
    objects = UserManager()
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
    )
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        choices=Gender.choices,
        help_text="User gender",
    )
    birthdate = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        choices=UserStatus.choices,
        help_text="User account status",
    )

    USERNAME_FIELD = "username"  # primary identifier for auth
    REQUIRED_FIELDS = []  # email kerak emas

    def __str__(self):
        return self.username

    def get_full_name(self) -> str:
        """Foydalanuvchining to'liq ismini qaytaradi"""
        parts = [self.first_name, self.middle_name, self.last_name]
        full_name = " ".join(filter(None, parts)).strip()
        return full_name if full_name else self.username
