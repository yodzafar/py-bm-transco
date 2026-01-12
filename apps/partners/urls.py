from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.partners.views import PartnerListAPIView

urlpatterns = [
    path("partners/", PartnerListAPIView.as_view(), name="partner-list"),
]
