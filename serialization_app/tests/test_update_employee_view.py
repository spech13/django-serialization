from django.test import TestCase

from serialization_app.tests.factories import DepartmentFactory, EmployeeFactory
from serialization_app.tests.update_object_view import UpdateObjectView


class UpdateEmployeeViewTestCase(UpdateObjectView, TestCase):
    url = "/serialization/employees/{id}/update"
    factory_class = EmployeeFactory
    data = {
        "first_name": "first-name-employee",
        "last_name": "last-name-employee",
        "age": 20,
    }

    def setUp(self):
        super().setUp()
        self.data["department_id"] = DepartmentFactory().id
