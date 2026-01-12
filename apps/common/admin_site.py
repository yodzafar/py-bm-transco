# apps/common/admin_site.py
from django.contrib import admin
from django.contrib.auth.models import Group, Permission


class CustomAdminSite(admin.AdminSite):
    site_header = "BM Transco Admin"
    site_title = "BM Transco Admin Portal"
    index_title = "Welcome to BM Transco Admin"


# Custom admin site yaratish
admin_site = CustomAdminSite(name="custom_admin")


# Group va Permission'ni unregister qilish (yashirish)
# Agar kerak bo'lsa, ularni qayta register qilish mumkin
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.unregister(Permission)
except admin.sites.NotRegistered:
    pass
