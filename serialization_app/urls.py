from django.urls import path

from serialization_app.views import (
    create_hex_nut,
    create_workstation,
    get_hex_nut,
    get_hex_nuts,
    get_workstation,
    get_workstations,
    update_hex_nut,
    update_workstation,
)

urlpatterns = [
    path("hex-nuts/get/", get_hex_nuts, name="get-hex-nuts"),
    path("hex-nuts/<int:id>/get/", get_hex_nut, name="get-hex-nut"),
    path("hex-nuts/create", create_hex_nut, name="create-hex-nuts"),
    path("hex-nuts/update", update_hex_nut, name="update-hex-nut"),
    path("workstations/get/", get_workstations, name="get-workstations"),
    path("workstations/<int:id>/get/", get_workstation, name="get-workstation"),
    path("workstations/create/", create_workstation, name="create-workstation"),
    path(
        "workstations/<int:id>/update/", update_workstation, name="update-workstation"
    ),
]
