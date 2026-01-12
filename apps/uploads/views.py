from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .models import Upload
from .serializers import UploadRequestSerializer, UploadResponseSerializer


class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return UploadRequestSerializer
        return UploadResponseSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @swagger_auto_schema(
        request_body=UploadRequestSerializer,
        responses={201: UploadResponseSerializer},
        operation_description="Upload a file (multipart/form-data).",
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save(created_by=request.user)

        try:
            instance.refresh_from_db()
        except Exception:
            pass

        # Return response using response serializer and include request context
        resp_serializer = UploadResponseSerializer(instance, context={'request': request})
        return Response(resp_serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        # Optional: if you want to remove file from storage on delete:
        try:
            if instance.file:
                instance.file.delete(save=False)
        except Exception:
            pass
        instance.delete()
