from django.contrib import admin
from django.utils.html import format_html

from apps.common.admin import BaseAdmin, BaseInline
from .models import Service, ServiceItem


class ServiceItemInline(BaseInline):
    model = ServiceItem
    extra = 1

    fields = (
        "title",
        "created_at",
    )

    readonly_fields = ("created_at",)

    show_change_link = True


@admin.register(Service)
class ServiceAdmin(BaseAdmin):
    list_display = (
        "image_preview",
        "name",
        "created_at",
        "is_active",
    )
    search_fields = ("name", "caption")
    inlines = [ServiceItemInline]
    list_display_links = ("image_preview", "name")
    readonly_fields = tuple(BaseAdmin.readonly_fields) + ("image_display",)

    fieldsets = (
        (
            "Service Information",
            {
                "fields": (
                    "name",
                    "caption",
                    "description",
                    "image",
                    "image_display",
                    "is_active",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": BaseAdmin.readonly_fields,
                "classes": ("collapse",),
            },
        ),
    )  # type: ignore

    @admin.display(description="Icon Preview")
    def image_preview(self, obj):
        """Small logo preview in list view"""
        if obj.image:
            return format_html(
                '<img src="{}" style="object-fit: contain; border-radius: 4px; height: 30px; width: auto;" />',
                obj.image.url,
            )
        return "-"

    @admin.display(description="Current Icon")
    def image_display(self, obj):
        """Large logo preview in detail view"""
        if obj.image:
            return format_html(
                '<div style="border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 10px; text-align: center;">'
                '<img src="{}" style="max-width: 300px; max-height: 300px;" />'
                "</div>",
                obj.image.url,
            )
        return format_html('<p style="color: #999;">No logo uploaded</p>')
