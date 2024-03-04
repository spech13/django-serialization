from django.test import TestCase

from serialization_app.tests.factories import WorkStationFactory
from serialization_app.tests.get_objects_view import GetObjectsView


class GetWorkStationsViewTestCase(GetObjectsView, TestCase):
    url = "/serialization/workstations/get"

    def setUp(self):
        self.expected_result = [
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
            for workstation in WorkStationFactory.create_batch(3)
        ]
