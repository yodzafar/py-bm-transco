from rest_framework import serializers

from apps.messages.models import ContactMessage, FreightQuote


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = (
            "id",
            "full_name",
            "company",
            "email",
            "phone",
            "message",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


class FreightQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreightQuote
        fields = (
            "id",
            "full_name",
            "email",
            "company",
            "equipment",
            "trailer_type",
            "commodity",
            "weight",
            "description",
            "pickup_zip_code",
            "dropoff_zip_code",
            "pickup_date",
            "dropoff_date",
            "created_at",
        )
        read_only_fields = ("id", "created_at")
