from http import HTTPStatus

from django.test import TestCase

from serialization_app.models import Employee
from serialization_app.tests.factories import DepartmentFactory

CONTENT_TYPE = "application/json"


class CreateDepartentViewTestCase(TestCase):
    url = "/serialization/employees/create"

    def setUp(self):
        self.data = {
            "first_name": "first-name-employee",
            "last_name": "last-name-employee",
            "age": 20,
        }

    def test_create_employee(self):
        response = self.client.post(self.url, content_type=CONTENT_TYPE, data=self.data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Employee.objects.get().department.name, "Free")

    def test_create_employee_by_department_id(self):
        self.data["department_id"] = DepartmentFactory().id
        response = self.client.post(self.url, content_type=CONTENT_TYPE, data=self.data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(
            Employee.objects.get().department.id, self.data["department_id"]
        )

    def test_create_employee_by_department(self):
        self.data["department"] = {
            "name": "department-name",
            "employees_number": 10,
            "description": "department-description",
        }
        response = self.client.post(self.url, content_type=CONTENT_TYPE, data=self.data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        employee = Employee.objects.get()
        self.assertDictEqual(
            self.data["department"],
            {
                "name": employee.department.name,
                "employees_number": employee.department.employees_number,
                "description": employee.department.description,
            },
        )

    def test_forbinded_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": "Method GET is forbinded"}
        )

    def test_decode_data_error(self):
        data = "some data"
        response = self.client.post(self.url, data=data, content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": f"Json decode error for {data}"}
        )
