from django.urls import path

from serialization_app.views import (
    create_hex_nut,
    get_hex_nut,
    get_hex_nuts,
    update_hex_nut,
)

urlpatterns = [
    path("hex-nuts/get/", get_hex_nuts, name="get-hex-nuts"),
    path("hex-nuts/<int:id>/get/", get_hex_nut, name="get-hex-nut"),
    path("hex-nuts/create", create_hex_nut, name="create-hex-nuts"),
    path("hex-nuts/update", update_hex_nut, name="update-hex-nut"),
]
