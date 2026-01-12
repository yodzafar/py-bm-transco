from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from .models import User


# ---------- Creation form (no password confirmation) ----------
class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput, required=True
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")

    def clean_password(self):
        pw = self.cleaned_data.get("password")
        if not pw:
            raise forms.ValidationError("This field is required.")
        return pw

    def save(self, commit=True):
        user = super().save(commit=False)
        pw = self.cleaned_data.get("password")
        if pw:
            user.set_password(pw)
        if commit:
            user.save()
        return user


# ---------- Change form (show hashed password read-only) ----------
class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored. You can change the "
            'password using <a href="../password/">this form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


# --------------- Admin registration --------------------
@admin.register(User)
class CustomUserAdmin(DjangoUserAdmin):
    add_form = CustomUserCreationForm  # creation form without confirmation
    form = CustomUserChangeForm  # change form
    model = User

    list_display = (
        "id",
        "first_name",
        "last_name",
        "username",
        "status",
        "is_staff",
        "is_active",
    )
    list_display_links = ("id", "username")
    search_fields = ("username", "first_name", "last_name")
    ordering = ("id",)
    list_filter = ("is_staff", "is_superuser", "is_active", "status", "groups")
    readonly_fields = (
        ("last_login", "date_joined")
        if hasattr(User, "date_joined")
        else ("last_login",)
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "middle_name",
                    "birthdate",
                    "gender",
                    "status",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    ("last_login", "date_joined")
                    if hasattr(User, "date_joined")
                    else ("last_login",)
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password", "is_staff", "is_active"),
            },
        ),
    )

    filter_horizontal = (
        "groups",
        "user_permissions",
    )
