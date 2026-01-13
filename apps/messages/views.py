from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.messages.models import ContactMessage, FreightQuote
from apps.messages.serializer import ContactMessageSerializer, FreightQuoteSerializer


class CreateContactMessageView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]


class FreightQuoteCreateView(generics.CreateAPIView):
    queryset = FreightQuote.objects.all()
    serializer_class = FreightQuoteSerializer
    permission_classes = [AllowAny]
