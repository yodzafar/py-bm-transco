from typing import Optional

from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.site_settings.models import SiteSettings
from apps.site_settings.serializer import SiteSettingsSerializer


class SiteSettingsView(generics.RetrieveAPIView):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [AllowAny]

    def get_object(self):  # type: ignore
        return self.queryset.first()
