from django.db import models

from apps.common.models import BaseModel
from apps.messages.utils import send_contact_email, send_freight_email


class ContactMessage(BaseModel):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    company = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.full_name} ({self.company if self.company else self.email})"

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            try:
                send_contact_email(self)
            except Exception as e:
                print(f"Contact Email Error: {e}")


class FreightQuote(BaseModel):
    # Sender Info
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=25, verbose_name="Phone Number")
    company = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Company"
    )

    # Cargo Info
    equipment = models.CharField(max_length=100, verbose_name="Equipment")
    trailer_type = models.CharField(max_length=100, verbose_name="Trailer Type")
    commodity = models.CharField(max_length=255, verbose_name="Commodity")
    weight = models.CharField(max_length=100, verbose_name="Weight")
    description = models.TextField(verbose_name="Description")

    # Logistics Info
    pickup_zip_code = models.CharField(max_length=20, verbose_name="Pickup Zip")
    pickup_date = models.DateField(verbose_name="Pickup Date")
    dropoff_zip_code = models.CharField(max_length=20, verbose_name="Delivery Zip")
    dropoff_date = models.DateField(verbose_name="Delivery Date")

    def __str__(self):
        return f"{self.full_name} - {self.commodity} ({self.pickup_zip_code} to {self.dropoff_zip_code})"

    class Meta:
        verbose_name = "Freight Quote"
        verbose_name_plural = "Freight Quotes"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            try:
                send_freight_email(self)
            except Exception as e:
                print(f"Error sending email: {e}")
