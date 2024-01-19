from http import HTTPStatus

from django.test import TestCase

from serialization_app.tests.factories import HexNutFactory


class GetHexNutsViewTestCase(TestCase):
    url = "/serialization/hex-nuts/get/"

    def test_success_get_hex_nuts(self):
        hex_nuts = HexNutFactory.create_batch(3)

        expected_result = [
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
            for hex_nut in hex_nuts
        ]

        response = self.client.get(self.url, content_type="application/json")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertListEqual(response.json(), expected_result)
