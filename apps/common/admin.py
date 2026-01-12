from typing import Any
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from apps.users.models import User

try:
    admin.site.unregister([Group])
except admin.sites.NotRegistered:
    pass


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
        "created_by_display",
        "updated_by_display",
        "deleted_by_display",
    )

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields = [f for f in fields if f not in self.readonly_fields]
        return [
            f for f in fields if f not in ("created_by", "updated_by", "deleted_by")
        ]

    def get_readonly_fields(self, request, obj=None):
        base = list(self.readonly_fields)
        for f in ("created_by", "updated_by", "deleted_by"):
            if f not in base:
                base.append(f)
        return tuple(base)

    def _user_display_text(self, user):
        if not user:
            return "-"
        full_name = None
        if hasattr(user, "get_full_name"):
            try:
                full_name = user.get_full_name().strip()
            except Exception:
                pass
        if full_name:
            return full_name
        return getattr(user, "username", None) or str(user)

    def _user_display_html(self, user):
        if not user or not getattr(user, "pk", None):
            return "-"
        text = self._user_display_text(user)
        username = getattr(user, "username", None)
        details = username or ""
        try:
            app_label = user._meta.app_label
            model_name = user._meta.model_name
            url = reverse(f"admin:{app_label}_{model_name}_change", args=(user.pk,))
            return format_html(
                '<a href="{}" target="_blank" rel="noopener noreferrer">'
                '<b>{}</b><br><small style="color: #555;">{}</small></a>',
                url,
                text,
                details,
            )
        except Exception:
            return text

    @admin.display(description="Created by")
    def created_by_display(self, obj):
        return self._user_display_html(getattr(obj, "created_by", None))

    @admin.display(description="Updated by")
    def updated_by_display(self, obj):
        return self._user_display_html(getattr(obj, "updated_by", None))

    @admin.display(description="Deleted by")
    def deleted_by_display(self, obj):
        return self._user_display_html(getattr(obj, "deleted_by", None))

    def save_model(self, request, obj, form, change):
        if not change and not getattr(obj, "created_by", None):
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if hasattr(obj, "deleted_by"):
            obj.deleted_by = request.user
            obj.save(update_fields=["deleted_by"])
        super().delete_model(request, obj)


class BaseInline(admin.TabularInline):
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
        "created_by_display",
        "updated_by_display",
        "deleted_by_display",
    )

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            return [f for f in fields if f not in self.readonly_fields]
        return fields

    def _user_display_text(self, user: User | None):
        if not user:
            return "-"
        full_name = None
        if hasattr(user, "get_full_name"):
            try:
                full_name = user.get_full_name().strip()
            except Exception:
                pass
        if full_name:
            return full_name
        return getattr(user, "username", None) or str(user)

    def _user_display_html(self, user: User | None):
        if not user or not getattr(user, "pk", None):
            return "-"
        text = self._user_display_text(user)
        username = getattr(user, "username", None)
        details = username or ""
        try:
            app_label = user._meta.app_label
            model_name = user._meta.model_name
            url = reverse(f"admin:{app_label}_{model_name}_change", args=(user.pk,))
            return format_html(
                '<a href="{}" target="_blank" rel="noopener noreferrer">'
                '<b>{}</b><br><small style="color: #555;">{}</small></a>',
                url,
                text,
                details,
            )
        except Exception:
            return text

    @admin.display(description="Created by")
    def created_by_display(self, obj):
        return self._user_display_html(getattr(obj, "created_by", None))

    @admin.display(description="Updated by")
    def updated_by_display(self, obj):
        return self._user_display_html(getattr(obj, "updated_by", None))

    @admin.display(description="Deleted by")
    def deleted_by_display(self, obj):
        return self._user_display_html(getattr(obj, "deleted_by", None))


class SingletonAdmin(admin.ModelAdmin):
    """
    Admin class for singleton models
    """

    def has_add_permission(self, request: HttpRequest) -> bool:
        # Faqat bitta instance bo'lsa, "Add" tugmasini ko'rsatmaslik
        return not self.model.objects.exists()

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        # Singleton'ni o'chirishni taqiqlash
        return False

    def changelist_view(  # type: ignore
        self, request: HttpRequest, extra_context: dict[str, Any] | None = None
    ) -> HttpResponse:
        # Agar instance mavjud bo'lsa, to'g'ridan-to'g'ri edit sahifasiga o'tish
        obj = self.model.objects.first()
        if obj:
            url = reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
                args=[obj.pk],
            )
            return HttpResponseRedirect(url)
        return super().changelist_view(request, extra_context)
