from django.test import TestCase

from serialization_app.models import HexNut
from serialization_app.tests.create_object_view import CreateObjectView


class CreateHexNutViewTestCase(CreateObjectView, TestCase):
    url = "/serialization/hex-nuts/create"
    model_class = HexNut
    data = {
        "designation": "hex-nut-name-1",
        "large_thread_pitch": 0.5,
        "small_thread_pitch": 0.5,
        "size": 0.5,
        "hight": 0.5,
        "e": 0.5,
        "mass_1000_pc": 0.5,
        "amout_pc_in_kg": 0.5,
    }
