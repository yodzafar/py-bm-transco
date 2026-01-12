from rest_framework import serializers

from apps.site_settings.models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            "homepage_title",
            "homepage_description",
            "driver_count",
            "partner_count",
            "contact_email",
            "contact_phone",
            "address",
            "location_url",
            "whatsapp_url",
            "telegram_url",
            "instagram_url",
            "facebook_url",
            "linkedin_url",
        ]

        read_only_fields = fields
