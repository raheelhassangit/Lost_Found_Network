from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Contact Info", {"fields": ("phone_number",)}),
    )
    list_display = ["username", "email", "phone_number", "is_staff"]


admin.site.register(User, UserAdmin)