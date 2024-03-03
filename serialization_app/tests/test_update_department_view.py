from http import HTTPStatus

from django.test import TestCase

from serialization_app.tests.factories import DepartmentFactory

CONTENT_TYPE = "application/json"


class UpdateDepartmentViewTestCase(TestCase):
    url = "/serialization/departments/{id}/update"

    def setUp(self):
        self.department = DepartmentFactory()
        self.data = {
            "name": "department-name",
            "employees_number": 10,
            "description": "department-description",
        }

    def test_update_department(self):
        response = self.client.patch(
            self.url.format(id=self.department.id),
            content_type=CONTENT_TYPE,
            data=self.data,
        )
        self.department.refresh_from_db()

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertDictEqual(
            self.data,
            {
                "name": self.department.name,
                "employees_number": self.department.employees_number,
                "description": self.department.description,
            },
        )

    def test_forbinded_method(self):
        response = self.client.get(self.url.format(id=self.department.id))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": "Method GET is forbinded"}
        )

    def test_decode_data_error(self):
        data = "some data"
        response = self.client.patch(
            self.url.format(id=self.department.id), data=data, content_type=CONTENT_TYPE
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": f"Json decode error for {data}"}
        )
