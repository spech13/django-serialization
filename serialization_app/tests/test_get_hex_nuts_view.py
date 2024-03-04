from django.test import TestCase

from serialization_app.tests.factories import HexNutFactory
from serialization_app.tests.get_objects_view import GetObjectsView


class GetHexNutsViewTestCase(GetObjectsView, TestCase):
    url = "/serialization/hex-nuts/get"

    def setUp(self):
        self.expected_result = [
            {
                "designation": hex_nut.designation,
                "large_thread_pitch": hex_nut.large_thread_pitch,
                "small_thread_pitch": hex_nut.small_thread_pitch,
                "size": hex_nut.size,
                "hight": hex_nut.hight,
                "e": hex_nut.e,
                "mass_1000_pc": hex_nut.mass_1000_pc,
                "amout_pc_in_kg": hex_nut.amout_pc_in_kg,
            }
            for hex_nut in HexNutFactory.create_batch(3)
        ]
