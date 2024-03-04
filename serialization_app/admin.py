from django.contrib import admin

from serialization_app.models import (
    Department,
    Employee,
    HexNut,
    Product,
    Store,
    User,
    WorkStation,
)


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


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name", "employees_number", "description"]
    readonly_fields = ("created_at", "updated_at")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "age", "department"]
    readonly_fields = ("created_at", "updated_at")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "password"]
    readonly_fields = ("created_at", "updated_at")
