from django.contrib import admin
from apps.common.admin import SingletonAdmin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    """
    Admin interface for Site Settings (Singleton)
    """

    fieldsets = (
        (
            "Homepage Settings",
            {"fields": ("homepage_title",), "description": "Homepage configuration"},
        ),
        (
            "Statistics",
            {
                "fields": ("driver_count", "partner_count"),
                "description": "Display statistics on the website",
            },
        ),
        (
            "Contact Information",
            {
                "fields": ("contact_email", "contact_phone", "address", "location_url"),
                "description": "Company contact details",
            },
        ),
        (
            "Social Media Links",
            {
                "fields": (
                    "whatsapp_url",
                    "telegram_url",
                    "instagram_url",
                    "facebook_url",
                    "linkedin_url",
                ),
                "classes": ("collapse",),
                "description": "Social media profile URLs",
            },
        ),
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    # List display
    list_display = ("homepage_title", "driver_count", "partner_count", "contact_email")
