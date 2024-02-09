from http import HTTPStatus

from django.test import TestCase

from serialization_app.tests.factories import WorkStationFactory


class GetWorkStationViewTestCase(TestCase):
    url = "/serialization/workstations/{id}/get/"

    def test_workstation_view(self):
        work_station = WorkStationFactory()

        response = self.client.get(
            self.url.format(id=work_station.id), content_type="application/json"
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertDictEqual(
            response.json(),
            {
                "id": work_station.id,
                "name": work_station.name,
                "ip_address": work_station.ip_address,
                "disk_capacity": work_station.disk_capacity,
                "ram": work_station.ram,
                "cpu": work_station.cpu,
                "serial_number": work_station.serial_number,
                "employee_name": work_station.employee_name,
            },
        )
