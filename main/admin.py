from django.contrib import admin
from .models import Unit, Direction, Location, Supplier
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "email")
    ordering = ("username",)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


from django.contrib import admin
from .models import (
    Unit, Supplier, Material, Direction, Location,
    MaterialIncome, IncomeItem,
    MaterialTransfer, TransferItem,
    MaterialWriteOff, WriteOffItem,
    Stock
)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "get_contact_name", "inn", "kpp")
    search_fields = ("name", "contact_last_name", "contact_first_name", "email", "inn")

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "article", "unit")
    search_fields = ("name", "article")

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "type", "is_active")
    search_fields = ("name", "address")

@admin.register(MaterialIncome)
class MaterialIncomeAdmin(admin.ModelAdmin):
    list_display = ("date", "document_number", "supplier", "responsible", "created_at")

@admin.register(IncomeItem)
class IncomeItemAdmin(admin.ModelAdmin):
    list_display = ("income", "material", "quantity", "direction", "location")

@admin.register(MaterialTransfer)
class MaterialTransferAdmin(admin.ModelAdmin):
    list_display = ("date", "document_number", "responsible", "created_at")

@admin.register(TransferItem)
class TransferItemAdmin(admin.ModelAdmin):
    list_display = ("transfer", "material", "quantity", "from_location", "to_location")

@admin.register(MaterialWriteOff)
class MaterialWriteOffAdmin(admin.ModelAdmin):
    list_display = ("date", "document_number", "reason", "responsible", "created_at")

@admin.register(WriteOffItem)
class WriteOffItemAdmin(admin.ModelAdmin):
    list_display = ("writeoff", "material", "quantity", "direction", "location")

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("material", "direction", "location", "quantity")