from django.test import TestCase

from serialization_app.tests.factories import HexNutFactory
from serialization_app.tests.get_object_view import GetObjectsView


class GetHexNutsViewTestCase(GetObjectsView, TestCase):
    url = "/serialization/hex-nuts/get"
    fields = [
        "designation",
        "large_thread_pitch",
        "small_thread_pitch",
        "size",
        "hight",
        "e",
        "mass_1000_pc",
        "amout_pc_in_kg",
    ]
    factory_class = HexNutFactory
