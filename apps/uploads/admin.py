# apps/uploads/admin.py
import os
import mimetypes
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Upload

@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "file_name",
        "file_ext",
        "file_mime_type",
        "file_size_display",
        "created_at_display",
        "file_preview",
    )
    list_display_links = ("id", "file_name")
    search_fields = ("file_name", "file_ext", "file_mime_type")
    list_filter = ("file_ext", "file_mime_type")
    readonly_fields = (
        "file_name",
        "file_url",
        "file_ext",
        "file_mime_type",
        "file_size",
        "file_preview",
    )

    # Pagination
    list_per_page = 25

    fieldsets = (
        (None, {
            "fields": ("file", "file_preview")
        }),
        (_("Metadata"), {
            "fields": (
                "file_name",
                "file_url",
                "file_ext",
                "file_mime_type",
                "file_size",
            ),
            "classes": ("collapse",),
        }),
    )

    def get_queryset(self, request):
        # select_related if you later add relations to Upload
        qs = super().get_queryset(request)
        return qs

    # ---------- helper display methods ----------
    @admin.display(description="Size")
    def file_size_display(self, obj):
        size = getattr(obj, "file_size", None)
        if not size:
            return "-"
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

    @admin.display(description="Created at")
    def created_at_display(self, obj):
        created = getattr(obj, "created_at", None)
        return created or "-"

    @admin.display(description="Preview / Download", ordering="file_name",)
    def file_preview(self, obj):
        if not obj or not obj.file:
            return "-"

        try:
            url = obj.file.url
        except Exception:
            url = obj.file.name

        mime = getattr(obj, "file_mime_type", None)
        if not mime:
            mime, _ = mimetypes.guess_type(obj.file_name or obj.file.name)

        if mime and mime.startswith("image/"):
            return format_html(
                '<a href="{}" target="_blank" rel="noopener noreferrer">'
                '<img src="{}" style="max-height:50px; max-width:70px; object-fit:contain; border:1px solid #ddd; padding:2px;" />'
                '</a>',
                url, url
            )

        display_name = obj.file_name or os.path.basename(obj.file.name)
        return format_html(
            '<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>',
            url, display_name
        )


