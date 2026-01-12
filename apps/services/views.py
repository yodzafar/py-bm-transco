from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.services.models import Service
from apps.services.serializer import ServiceSerializer

# Create your views here.


class ServiceListAPIView(generics.ListAPIView):

    queryset = Service.objects.filter(is_active=True).order_by("id")
    pagination_class = None
    permission_classes = [AllowAny]
    serializer_class = ServiceSerializer
    ordering_fields = ["id"]
    ordering = ["id"]
