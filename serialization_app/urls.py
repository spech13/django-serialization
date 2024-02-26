from django.urls import path

from serialization_app.views import (
    create_hex_nut,
    create_product,
    create_store,
    create_workstation,
    get_hex_nut,
    get_hex_nuts,
    get_workstation,
    get_workstations,
    partial_update_store,
    update_hex_nut,
    update_product,
    update_store,
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
    path("stores/create", create_store, name="create-store"),
    path("stores/<int:id>/update", update_store, name="update-store"),
    path(
        "stores/<int:id>/partial-update",
        partial_update_store,
        name="partial-update-store",
    ),
    path("products/create", create_product, name="create-product"),
    path("products/<int:id>/update", update_product, name="update-product"),
]
