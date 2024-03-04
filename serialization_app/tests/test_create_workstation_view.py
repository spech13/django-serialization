from http import HTTPStatus

from django.test import TestCase

from serialization_app.models import WorkStation
from serialization_app.serializers import (
    WORK_STATION_IP_ADDRESS_PATTERN,
    WORK_STATION_NAME_PATTERN,
    WORK_STATION_SERIAL_NUMBER_PATTERN,
)
from serialization_app.tests.create_object_view import CONTENT_TYPE, CreateObjectView


class CreateWrokStationViewTestCase(CreateObjectView, TestCase):
    url = "/serialization/workstations/create"
    model_class = WorkStation
    data = {
        "name": "WS-0001",
        "ip_address": "192.168.12.9",
        "disk_capacity": 10,
        "ram": 4,
        "cpu": 2,
        "serial_number": "KKDJ-SKLD-DOKS-LSKD",
        "employee_name": "Mark Josev",
    }

    def test_not_valid_name(self):
        response = self.client.post(
            self.url,
            content_type=CONTENT_TYPE,
            data=self.get_and_update_data({"name": "WS-001"}),
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "validation_errors": {
                    "name": "name field must match the pattern "
                    f"{WORK_STATION_NAME_PATTERN}. Example WS-1296"
                }
            },
        )

    def test_not_valid_ip_address(self):
        data = self.get_and_update_data({"ip_address": "192.xxx.12.9"})

        response = self.client.post(self.url, content_type=CONTENT_TYPE, data=data)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "validation_errors": {
                    "ip_address": "ip_address field must match the pattern "
                    f"{WORK_STATION_IP_ADDRESS_PATTERN}"
                }
            },
        )

        error_number = 300
        data["ip_address"] = f"192.168.12.{error_number}"
        response = self.client.post(self.url, content_type=CONTENT_TYPE, data=data)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "validation_errors": {
                    "ip_address": f"number {error_number} must be less 255"
                }
            },
        )

    def test_not_valid_serial_number(self):
        response = self.client.post(
            self.url,
            content_type=CONTENT_TYPE,
            data=self.get_and_update_data({"serial_number": "JFKD-XXX-DJFK-LLL"}),
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "validation_errors": {
                    "serial_number": "serial_number field must match the pattern "
                    f"{WORK_STATION_SERIAL_NUMBER_PATTERN}"
                }
            },
        )

    def test_not_valid_cpu_ram_disk_capacity(self):
        response = self.client.post(
            self.url,
            content_type=CONTENT_TYPE,
            data=self.get_and_update_data({"cpu": 4, "ram": 2}),
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "validation_errors": {
                    "non_field_errors": "validation data must satisfy "
                    "the requirement cpu < rum < disck_capacity"
                }
            },
        )
