from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UploadViewSet

router = DefaultRouter()
router.register(r'uploads', UploadViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
