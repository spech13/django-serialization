from http import HTTPStatus

from django.test import TestCase

from serialization_app.models import WorkStation
from serialization_app.serializers import (
    WORK_STATION_IP_ADDRESS_PATTERN,
    WORK_STATION_NAME_PATTERN,
    WORK_STATION_SERIAL_NUMBER_PATTERN,
)


class CreateWrokStationViewTestCase(TestCase):
    url = "/serialization/workstations/create/"

    def setUp(self):
        self.data = {
            "name": "WS-0001",
            "ip_address": "192.168.12.9",
            "disk_capacity": 10,
            "ram": 4,
            "cpu": 2,
            "serial_number": "KKDJ-SKLD-DOKS-LSKD",
            "employee_name": "Mark Josev",
        }

    def test_create_workstation_view(self):
        response = self.client.post(
            self.url, content_type="application/json", data=self.data
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        workstation = WorkStation.objects.get()
        self.assertDictEqual(
            self.data,
            {
                "name": workstation.name,
                "ip_address": workstation.ip_address,
                "disk_capacity": workstation.disk_capacity,
                "ram": workstation.ram,
                "cpu": workstation.cpu,
                "serial_number": workstation.serial_number,
                "employee_name": workstation.employee_name,
            },
        )

    def test_not_valid_name(self):
        self.data["name"] = "WS-001"

        response = self.client.post(
            self.url, content_type="application/json", data=self.data
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
        self.data["ip_address"] = "192.xxx.12.9"
        response = self.client.post(
            self.url, content_type="application/json", data=self.data
        )

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
        self.data["ip_address"] = f"192.168.12.{error_number}"
        response = self.client.post(
            self.url, content_type="application/json", data=self.data
        )

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
        self.data["serial_number"] = "JFKD-XXX-DJFK-LLL"

        response = self.client.post(
            self.url, content_type="application/json", data=self.data
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
        self.data["cpu"] = 4
        self.data["ram"] = 2

        response = self.client.post(
            self.url, content_type="application/json", data=self.data
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
