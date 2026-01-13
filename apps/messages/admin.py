from django.contrib import admin

from apps.common.admin import BaseAdmin

from .models import ContactMessage, FreightQuote


@admin.register(ContactMessage)
class ContactMessageAdmin(BaseAdmin):
    """
    Admin interface for Contact Messages
    """

    list_display = ("full_name", "email", "company", "phone", "created_at")

    list_display_links = ("full_name", "email")

    search_fields = ("full_name", "email", "company", "message", "phone")

    list_filter = ("created_at", "company")

    fieldsets = (
        (
            "Sender Information",
            {"fields": ("full_name", "company", "email", "phone")},
        ),
        (
            "Message Content",
            {"fields": ("message",)},
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

    readonly_fields = tuple(BaseAdmin.readonly_fields)

    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False


@admin.register(FreightQuote)
class FreightQuoteAdmin(BaseAdmin):
    list_display = (
        "full_name",
        "email",
        "phone",
        "trailer_type",
        "pickup_date",
        "dropoff_date",
        "created_at",
    )
    list_filter = ("pickup_date", "dropoff_date", "trailer_type", "created_at")
    search_fields = (
        "full_name",
        "email",
        "commodity",
        "pickup_zip_code",
        "dropoff_zip_code",
    )

    fieldsets = (
        (
            "Contact Details",
            {"fields": ("full_name", "email", "phone", "company")},
        ),
        (
            "Shipment Details",
            {
                "fields": (
                    "equipment",
                    "trailer_type",
                    "commodity",
                    "weight",
                    "description",
                )
            },
        ),
        (
            "Logistics / Timeline",
            {
                "fields": (
                    "pickup_zip_code",
                    "pickup_date",
                    "dropoff_zip_code",
                    "dropoff_date",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": ("id", "created_at", "updated_at", "created_by_display"),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = tuple(BaseAdmin.readonly_fields)

    def has_add_permission(self, request):
        return False
