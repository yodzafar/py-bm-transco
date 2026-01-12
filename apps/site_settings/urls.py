from django.urls import path
from apps.site_settings.views import SiteSettingsView


urlpatterns = [
    path("site-settings/", SiteSettingsView.as_view(), name="site-settings"),
]
