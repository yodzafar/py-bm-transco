from django.contrib.auth.models import BaseUserManager
from apps.users.enums import UserStatus


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username=None, password=None, **extra_fields):
        if not username:
            raise ValueError("User must have a username")

        username = username.strip() if username else None
        extra_fields.setdefault("status", UserStatus.ACTIVE)

        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("status", UserStatus.ACTIVE)
        return self._create_user(username=username, password=password, **extra_fields)

    def create_superuser(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("status", UserStatus.ACTIVE)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username=username, password=password, **extra_fields)

    def active(self):
        return self.filter(status=UserStatus.ACTIVE, deleted_at__isnull=True)

    def inactive(self):
        return self.filter(status=UserStatus.INACTIVE, deleted_at__isnull=True)

    def deleted(self):
        return self.filter(status=UserStatus.DELETED)
