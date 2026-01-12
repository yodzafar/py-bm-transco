from django.db import models
from apps.common.models import BaseModel


class Service(BaseModel):
    name = models.CharField(max_length=255)
    caption = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="services/images/", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ServiceItem(BaseModel):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.service.name} - {self.title}"
