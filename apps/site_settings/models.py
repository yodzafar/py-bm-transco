from django.db import models

from apps.common.models import SingletonModel


# Create your models here.
class SiteSettings(SingletonModel):
    homepage_title = models.TextField(max_length=255, null=True, blank=True)
    homepage_description = models.TextField(null=True, blank=True)
    driver_count = models.PositiveIntegerField(default=0)
    partner_count = models.PositiveIntegerField(default=0)

    # Contact information
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    location_url = models.URLField(null=True, blank=True)

    # Social media links
    whatsapp_url = models.URLField(null=True, blank=True)
    telegram_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
