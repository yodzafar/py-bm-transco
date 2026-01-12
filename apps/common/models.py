from django.db import models
from django.conf import settings
from django.forms import ValidationError
from django.utils import timezone
from .current_user import get_current_user
from .managers import SoftDeleteManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        user = get_current_user()
        if (
            not getattr(self, "pk", None)
            and not self.created_by
            and user
            and getattr(user, "is_authenticated", False)
        ):
            try:
                self.created_by = user
            except Exception:
                pass
        if user and getattr(user, "is_authenticated", False):
            try:
                self.updated_by = user
            except Exception:
                pass
        super().save(*args, **kwargs)

    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_deleted_by",
        null=True,
        blank=True,
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # hamma yozuvlar uchun oddiy manager

    def delete(self, using=None, keep_parents=False, user=None):
        user = user or get_current_user()
        self.deleted_at = timezone.now()
        if user and getattr(user, "is_authenticated", False):
            try:
                self.deleted_by = user
            except Exception:
                pass
        # update relevant fields only
        self.save(
            update_fields=["deleted_at", "deleted_by", "updated_at", "updated_by"]
        )
        return 1, {self._meta.label: 1}

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)

    def restore(self, user=None):
        self.deleted_at = None
        self.deleted_by = None
        user = user or get_current_user()
        if user and getattr(user, "is_authenticated", False):
            try:
                self.updated_by = user
            except Exception:
                pass
        self.save()


class SingletonModel(BaseModel):
    """
    Abstract base class for models that should only have one instance.
    """

    class Meta(BaseModel.Meta):
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        self.deleted_at = None
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Singleton model cannot be deleted")

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        if obj.deleted_at:
            obj.deleted_at = None
            obj.save()
        return obj
