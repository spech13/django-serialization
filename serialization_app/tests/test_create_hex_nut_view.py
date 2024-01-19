import json
from http import HTTPStatus

from django.test import TestCase

from serialization_app.models import HexNut


class CreateHexNutViewTestCase(TestCase):
    url = "/serialization/hex-nuts/create"

    def setUp(self):
        self.data = {
            "designation": "hex-nut-name-1",
            "large_thread_pitch": 0.5,
            "small_thread_pitch": 0.5,
            "size": 0.5,
            "hight": 0.5,
            "e": 0.5,
            "mass_1000_pc": 0.5,
            "amout_pc_in_kg": 0.5,
        }

    def test_success_create_hex_nut(self):
        self.assertFalse(HexNut.objects.filter(designation=self.data["designation"]))

        response = self.client.post(
            self.url,
            data=f"json_data=[{json.dumps(self.data)}]",
            content_type="application/x-www-form-urlencoded",
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        HexNut.objects.get(designation=self.data["designation"])

    def test_failed_data_loads(self):
        response = self.client.post(
            self.url,
            data=f"json_data=[{self.data}]",
            content_type="application/x-www-form-urlencoded",
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.content.decode(), f"Failed data loads: [{self.data}]")

    def test_data_is_not_valid(self):
        response = self.client.post(
            self.url,
            data=f"json_data={json.dumps(self.data)}",
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response.content.decode(), f"Data is not valid: {json.dumps(self.data)}"
        )
