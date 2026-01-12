from rest_framework import serializers

from apps.partners.models import Partner
from config import settings


class PartnerSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Partner
        fields = [
            "id",
            "name",
            "description",
            "website_url",
            "logo_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_logo_url(self, obj):
        if obj.logo:
            return obj.logo.url
        return None
