from http import HTTPStatus

from django.test import TestCase

from serialization_app.serializers import (
    WORK_STATION_IP_ADDRESS_PATTERN,
    WORK_STATION_NAME_PATTERN,
    WORK_STATION_SERIAL_NUMBER_PATTERN,
)
from serialization_app.tests.factories import WorkStationFactory
from serialization_app.tests.update_object_view import UpdateObjectView


class UpdateWorkStationViewTestCase(UpdateObjectView, TestCase):
    url = "/serialization/workstations/{id}/update"
    factory_class = WorkStationFactory
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
        response = self.client.patch(
            self.url.format(id=WorkStationFactory().id),
            content_type="application/json",
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
        workstation = WorkStationFactory()

        response = self.client.patch(
            self.url.format(id=workstation.id),
            content_type="application/json",
            data=self.get_and_update_data({"ip_address": "192.xxx.12.9"}),
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
        response = self.client.patch(
            self.url.format(id=workstation.id),
            content_type="application/json",
            data=self.get_and_update_data({"ip_address": f"192.168.12.{error_number}"}),
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
        response = self.client.patch(
            self.url.format(id=WorkStationFactory().id),
            content_type="application/json",
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
