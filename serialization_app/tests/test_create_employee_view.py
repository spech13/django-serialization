from http import HTTPStatus

from django.test import TestCase

from serialization_app.models import Employee
from serialization_app.tests.create_object_view import CONTENT_TYPE, CreateObjectView
from serialization_app.tests.factories import DepartmentFactory


class CreateEmployeetViewTestCase(CreateObjectView, TestCase):
    url = "/serialization/employees/create"
    model_class = Employee
    data = {
        "first_name": "first-name-employee",
        "last_name": "last-name-employee",
        "age": 20,
    }

    def test_create_employee_with_default_department(self):
        response = self.client.post(self.url, content_type=CONTENT_TYPE, data=self.data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Employee.objects.get().department.name, "Free")

    def test_create_employee_by_department_id(self):
        data = self.get_and_update_data({"department_id": DepartmentFactory().id})

        response = self.client.post(self.url, content_type=CONTENT_TYPE, data=data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Employee.objects.get().department.id, data["department_id"])

    def test_create_employee_by_department(self):
        data = self.get_and_update_data(
            {
                "department": {
                    "name": "department-name",
                    "employees_number": 10,
                    "description": "department-description",
                }
            }
        )
        response = self.client.post(self.url, content_type=CONTENT_TYPE, data=data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        employee = Employee.objects.get()
        self.assertDictEqual(
            data["department"],
            {
                "name": employee.department.name,
                "employees_number": employee.department.employees_number,
                "description": employee.department.description,
            },
        )
