from http import HTTPStatus

from django.test import TestCase

from serialization_app.tests.factories import HexNutFactory


class GetHexNutViewTestCase(TestCase):
    url = "/serialization/hex-nuts/{nut_id}/get/"

    def test_success_get_hex_nut(self):
        hex_nut = HexNutFactory()

        response = self.client.get(
            self.url.format(nut_id=hex_nut.id), content_type="application/json"
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertDictEqual(
            response.json(),
            {
                "designation": hex_nut.designation,
                "large_thread_pitch": hex_nut.large_thread_pitch,
                "small_thread_pitch": hex_nut.small_thread_pitch,
                "size": hex_nut.size,
                "hight": hex_nut.hight,
                "e": hex_nut.e,
                "mass_1000_pc": hex_nut.mass_1000_pc,
                "amout_pc_in_kg": hex_nut.amout_pc_in_kg,
            },
        )

    def test_get_hex_nut_does_not_exist(self):
        response = self.client.get(
            self.url.format(nut_id="1"), content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
