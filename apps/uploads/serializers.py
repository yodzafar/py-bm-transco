from django.conf import settings
from rest_framework import serializers
from .models import Upload
from ..users.serializers.short_user import ShortUserSerializer


class UploadRequestSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = Upload
        fields = ['file']


class UploadResponseSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField(read_only=True)
    created_by = ShortUserSerializer(read_only=True)

    class Meta:
        model = Upload
        fields = [
            'id',
            'file_name',
            'file_url',
            'file_ext',
            'file_mime_type',
            'file_size',
            'created_at',
            'created_by'
        ]
        read_only_fields = fields

    def get_file_url(self, obj):
        if not obj.file:
            return ""

        storage_url = None
        try:
            if hasattr(obj.file, "url"):
                storage_url = obj.file.url
        except Exception:
            storage_url = None

        request = self.context.get("request")

        if storage_url:
            if request is not None:
                try:
                    return request.build_absolute_uri(storage_url)
                except Exception:
                    pass

            if storage_url.startswith(("http://", "https://")):
                return storage_url

            domain = getattr(settings, "DEFAULT_DOMAIN", "").rstrip("/")
            if domain:
                if not storage_url.startswith("/"):
                    storage_url = "/" + storage_url
                return f"{domain}{storage_url}"

            return storage_url

        stored_name = getattr(obj.file, "name", "")
        if not stored_name:
            return ""

        if request is not None:
            try:
                return request.build_absolute_uri(stored_name)
            except Exception:
                pass

        domain = getattr(settings, "DEFAULT_DOMAIN", "")
        if domain:
            if not stored_name.startswith("/"):
                stored_name = "/" + stored_name
            return f"{domain.rstrip('/')}{stored_name}"

        return stored_name
