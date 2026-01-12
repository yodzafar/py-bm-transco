from rest_framework import serializers

from apps.services.models import Service
from config import settings


class ServiceSerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    def get_icon_url(self, obj):
        if obj.image:
            return f"{settings.API_HOST}{obj.image.url}"
        return None

    def get_items(self, obj):
        return [{"id": item.id, "title": item.title} for item in obj.items.all()]

    class Meta:
        model = Service
        fields = [
            "id",
            "name",
            "caption",
            "description",
            "icon_url",
            "is_active",
            "created_at",
            "updated_at",
            "items",
        ]
        read_only_fields = fields
