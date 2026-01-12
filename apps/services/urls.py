from django.urls import path
from apps.services.views import ServiceListAPIView


urlpatterns = [
    path("services/", ServiceListAPIView.as_view()),
]
