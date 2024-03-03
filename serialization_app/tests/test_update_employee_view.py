from http import HTTPStatus

from django.test import TestCase

from serialization_app.tests.factories import DepartmentFactory, EmployeeFactory

CONTENT_TYPE = "application/json"


class UpdateDepartmentViewTestCase(TestCase):
    url = "/serialization/employees/{id}/update"

    def setUp(self):
        self.employee = EmployeeFactory()
        self.data = {
            "first_name": "first-name-employee",
            "last_name": "last-name-employee",
            "age": 20,
        }

    def test_update_employee(self):
        response = self.client.patch(
            self.url.format(id=self.employee.id),
            content_type=CONTENT_TYPE,
            data=self.data,
        )
        self.employee.refresh_from_db()

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertDictEqual(
            self.data,
            {
                "first_name": self.employee.first_name,
                "last_name": self.employee.last_name,
                "age": self.employee.age,
            },
        )

    def test_update_employee_department(self):
        self.data["department_id"] = DepartmentFactory().id

        response = self.client.patch(
            self.url.format(id=self.employee.id),
            content_type=CONTENT_TYPE,
            data=self.data,
        )
        self.employee.refresh_from_db()

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertDictEqual(
            self.data,
            {
                "first_name": self.employee.first_name,
                "last_name": self.employee.last_name,
                "age": self.employee.age,
                "department_id": self.employee.department.id,
            },
        )

    def test_forbinded_method(self):
        response = self.client.get(self.url.format(id=self.employee.id))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": "Method GET is forbinded"}
        )

    def test_decode_data_error(self):
        data = "some data"
        response = self.client.patch(
            self.url.format(id=self.employee.id), data=data, content_type=CONTENT_TYPE
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": f"Json decode error for {data}"}
        )
