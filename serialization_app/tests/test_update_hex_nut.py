from django.test import TestCase

from serialization_app.tests.factories import HexNutFactory
from serialization_app.tests.update_object_view import UpdateObjectView


class UpdateHexNut(UpdateObjectView, TestCase):
    url = "/serialization/hex-nuts/{id}/update"
    factory_class = HexNutFactory
    data = {
        "designation": "new-designation",
        "large_thread_pitch": 0.5,
        "small_thread_pitch": 0.5,
        "size": 0.5,
        "hight": 0.5,
        "e": 0.5,
        "mass_1000_pc": 0.5,
        "amout_pc_in_kg": 0.5,
    }
