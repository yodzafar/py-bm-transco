from rest_framework import generics, filters
from rest_framework.permissions import AllowAny

from apps.partners.models import Partner
from apps.partners.serializer import PartnerSerializer


class PartnerListAPIView(generics.ListAPIView):
    queryset = Partner.objects.all().order_by("id")
    serializer_class = PartnerSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    ordering_fields = ["id"]
    ordering = ["id"]
