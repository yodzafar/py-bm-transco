from django.db import models
from apps.common.models import BaseModel


# Create your models here.
class Partner(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    logo = models.ImageField(upload_to="partners/logos/")

    def __str__(self):
        return self.name
