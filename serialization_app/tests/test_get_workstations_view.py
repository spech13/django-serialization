from django.test import TestCase

from serialization_app.tests.factories import WorkStationFactory
from serialization_app.tests.get_object_view import GetObjectsView


class GetWorkStationsViewTestCase(GetObjectsView, TestCase):
    url = "/serialization/workstations/get"
    fields = [
        "id",
        "name",
        "ip_address",
        "disk_capacity",
        "ram",
        "cpu",
        "serial_number",
        "employee_name",
    ]
    factory_class = WorkStationFactory
