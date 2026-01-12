import mimetypes
import os
import uuid
from django.db import models
from django.utils import timezone
from apps.common.models import BaseModel


def upload_path(instance, filename):
    ts = timezone.now().strftime("%Y%m%d_%H%M%S")
    ext = os.path.splitext(filename)[1]
    new_filename = f"{ts}_{uuid.uuid4().hex}{ext}"
    return f"uploads/{new_filename}"


class Upload(BaseModel):
    file = models.FileField(upload_to=upload_path)
    file_name = models.CharField(max_length=255, blank=True)  # original filename
    file_url = models.CharField(max_length=1024, blank=True)
    file_ext = models.CharField(max_length=10, blank=True)
    file_mime_type = models.CharField(max_length=255, blank=True)
    file_size = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        original_name = None
        if getattr(self.file, "name", None):
            original_name = os.path.basename(self.file.name)

        print(original_name)

        if is_new:
            super().save(*args, **kwargs)

        changed = False

        if self.file:
            if original_name:
                name = original_name
            else:
                name = os.path.basename(getattr(self.file, "name", "") or "")

            if self.file_name != name:
                self.file_name = name
                changed = True

            _, ext = os.path.splitext(getattr(self.file, "name", "") or "")
            ext = ext.lower().lstrip(".") if ext else ""
            if ext and self.file_ext != ext:
                self.file_ext = ext
                changed = True

            mime = None
            try:
                uploaded_obj = getattr(self.file, "file", None)
                mime = getattr(uploaded_obj, "content_type", None)
            except Exception:
                mime = None

            if not mime:
                guessed, _ = mimetypes.guess_type(getattr(self.file, "name", ""))
                mime = guessed

            if mime and self.file_mime_type != mime:
                self.file_mime_type = mime
                changed = True

            size = getattr(self.file, "size", None)
            if size is None:
                try:
                    self.file.seek(0, os.SEEK_END)
                    size = self.file.tell()
                    self.file.seek(0)
                except Exception:
                    size = None

            if size is not None and self.file_size != size:
                self.file_size = size
                changed = True

            try:
                url = self.file.url
            except Exception:
                url = getattr(self.file, "name", "")

            if self.file_url != url:
                self.file_url = url
                changed = True

        if changed:
            update_fields = (
                "file_name",
                "file_url",
                "file_ext",
                "file_mime_type",
                "file_size",
            )
            super().save(update_fields=update_fields)
        elif not is_new:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name or "Unnamed File"
