from django.contrib import admin

from serialization_app.models import HexNut, Product, Store, WorkStation


@admin.register(HexNut)
class HexNutAdmin(admin.ModelAdmin):
    list_display = [
        "designation",
        "large_thread_pitch",
        "small_thread_pitch",
        "size",
        "hight",
        "e",
        "mass_1000_pc",
        "amout_pc_in_kg",
    ]
    readonly_fields = ("created_at", "updated_at")


@admin.register(WorkStation)
class WorkStationAdmin(admin.ModelAdmin):
    list_display = ["name", "ip_address", "employee_name"]
    readonly_fields = ("created_at", "updated_at")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "store", "category", "price", "vendor_code"]
    readonly_fields = ("created_at", "updated_at")


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ["address", "manager_name", "manager_number"]
    readonly_fields = ("created_at", "updated_at")
