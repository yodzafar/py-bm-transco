from django.db import models

class UserStatus(models.TextChoices):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DELETED = 'deleted'

class Gender(models.TextChoices):
    MALE = 'male'
    FEMALE = 'female'