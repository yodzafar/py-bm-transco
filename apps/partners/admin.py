from django.contrib import admin
from django.utils.html import format_html

from apps.common.admin import BaseAdmin

from .models import Partner


@admin.register(Partner)
class PartnerAdmin(BaseAdmin):
    """
    Admin interface for Partners
    """

    list_display = ("logo_preview", "name", "website_url", "created_at")
    list_display_links = ("logo_preview", "name")
    search_fields = ("name", "description", "website_url")
    list_filter = ("created_at", "updated_at")

    fieldsets = (
        (
            "Partner Information",
            {"fields": ("name", "description", "website_url", "logo", "logo_display")},
        ),
        (
            "System Information",
            {
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                    "deleted_at",
                    "created_by_display",
                    "updated_by_display",
                    "deleted_by_display",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = tuple(BaseAdmin.readonly_fields) + ("logo_display",)

    @admin.display(description="Logo Preview")
    def logo_preview(self, obj):
        """Small logo preview in list view"""
        if obj.logo:
            return format_html(
                '<img src="{}" style="object-fit: contain; border-radius: 4px; height: 30px; width: auto;" />',
                obj.logo.url,
            )
        return "-"

    @admin.display(description="Current Logo")
    def logo_display(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px; object-fit: contain;" />',
                obj.logo.url,
            )
        return "No logo"  # Oddiy string
