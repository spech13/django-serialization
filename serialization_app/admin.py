from django.contrib import admin

from serialization_app.models import HexNut, WorkStation


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


@admin.register(WorkStation)
class WorkStationAdmin(admin.ModelAdmin):
    list_display = ["name", "ip_address", "employee_name"]
