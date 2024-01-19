from django.test import TestCase
import json
from serialization_app.tests.factories import HexNutFactory
from http import HTTPStatus

class UpdateHexNut(TestCase):
    url = "/serialization/hex-nuts/update"

    def setUp(self):
        self.hex_nut = HexNutFactory()
        self.data = {
            "designation": self.hex_nut.designation,
            "large_thread_pitch": self.hex_nut.large_thread_pitch + 0.5,
            "small_thread_pitch": self.hex_nut.small_thread_pitch + 0.5,
            "size": self.hex_nut.size + 0.5,
            "hight": self.hex_nut.hight + 0.5,
            "e": self.hex_nut.e + 0.5,
            "mass_1000_pc": self.hex_nut.mass_1000_pc + 0.5,
            "amout_pc_in_kg": self.hex_nut.amout_pc_in_kg + 0.5,
        }

    def test_success_update_hex_nut(self):
        data = f"nut_id={self.hex_nut.id}&json_data={json.dumps(self.data)}"

        response = self.client.patch(self.url, data=data, content_type="application/x-www-form-urlencoded")
        self.hex_nut.refresh_from_db()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content.decode(), f'Successful reques: {json.dumps(self.data)}')

        self.assertDictEqual(self.data, {
            "designation": self.hex_nut.designation,
            "large_thread_pitch": self.hex_nut.large_thread_pitch,
            "small_thread_pitch": self.hex_nut.small_thread_pitch,
            "size": self.hex_nut.size,
            "hight": self.hex_nut.hight,
            "e": self.hex_nut.e,
            "mass_1000_pc": self.hex_nut.mass_1000_pc,
            "amout_pc_in_kg": self.hex_nut.amout_pc_in_kg,
        })

    def test_failed_data_loads(self):
        response = self.client.post(
            self.url,
            data=f"nut_id={self.hex_nut.id}&json_data={self.data}",
            content_type="application/x-www-form-urlencoded",
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.content.decode(), f"Failed data loads: {self.data}")

    def test_data_is_not_valid(self):
            response = self.client.post(
                self.url,
                data=f"nut_id={self.hex_nut.id}&json_data=[{json.dumps(self.data)}]",
                content_type="application/x-www-form-urlencoded",
            )
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertEqual(
                response.content.decode(), f"Data is not valid: [{json.dumps(self.data)}]"
            )