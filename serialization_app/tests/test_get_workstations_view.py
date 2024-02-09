from http import HTTPStatus

from django.test import TestCase

from serialization_app.tests.factories import WorkStationFactory


class GetWorkStationsViewTestCase(TestCase):
    url = "/serialization/workstations/get/"

    def test_get_workstations_view(self):
        workstations = WorkStationFactory.create_batch(3)

        expected_result = [
            {
                "id": workstation.id,
                "name": workstation.name,
                "ip_address": workstation.ip_address,
                "disk_capacity": workstation.disk_capacity,
                "ram": workstation.ram,
                "cpu": workstation.cpu,
                "serial_number": workstation.serial_number,
                "employee_name": workstation.employee_name,
            }
            for workstation in workstations
        ]

        response = self.client.get(self.url, content_type="application/json")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertListEqual(response.json(), expected_result)
