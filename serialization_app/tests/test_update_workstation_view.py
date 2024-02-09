from http import HTTPStatus

from django.test import TestCase

from serialization_app.tests.factories import WorkStationFactory
from serialization_app.serializers import WORK_STATION_NAME_PATTERN, WORK_STATION_IP_ADDRESS_PATTERN, WORK_STATION_SERIAL_NUMBER_PATTERN


class UpdateWorkStationViewTestCase(TestCase):
    url = "/serialization/workstations/{id}/update/"

    def setUp(self):
        self.workstation = WorkStationFactory()
        self.data = {
            "name": "WS-0001",
            "ip_address": "192.168.12.9",
            "disk_capacity": 10,
            "ram": 4,
            "cpu": 2,
            "serial_number": "KKDJ-SKLD-DOKS-LSKD",
            "employee_name": "Mark Josev",
        }

    def test_update_workstation_view(self):

        response = self.client.patch(
            self.url.format(id=self.workstation.id),
            content_type="application/json",
            data=self.data,
        )
        self.workstation.refresh_from_db()

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertDictEqual(
            self.data,
            {
                "name": self.workstation.name,
                "ip_address": self.workstation.ip_address,
                "disk_capacity": self.workstation.disk_capacity,
                "ram": self.workstation.ram,
                "cpu": self.workstation.cpu,
                "serial_number": self.workstation.serial_number,
                "employee_name": self.workstation.employee_name,
            },
        )

    def test_not_valid_name(self):
        self.data["name"] = "WS-001"

        response = self.client.patch(
            self.url.format(id=self.workstation.id),
            content_type="application/json",
            data=self.data,
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

        response = self.client.patch(
            self.url.format(id=self.workstation.id),
            content_type="application/json",
            data=self.data,
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
        response = self.client.patch(
            self.url.format(id=self.workstation.id), content_type="application/json", data=self.data
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

        response = self.client.patch(
            self.url.format(id=self.workstation.id),
            content_type="application/json",
            data=self.data,
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
