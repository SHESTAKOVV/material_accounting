from django.contrib import admin
from .models import Unit
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "email")
    ordering = ("username",)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)