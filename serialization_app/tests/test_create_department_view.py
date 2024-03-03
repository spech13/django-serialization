from http import HTTPStatus

from django.test import TestCase

from serialization_app.models import Department

CONTENT_TYPE = "application/json"


class CreateDepartentViewTestCase(TestCase):
    url = "/serialization/departments/create"

    def setUp(self):
        self.data = {
            "name": "department-name",
            "employees_number": 10,
            "description": "department-description",
        }

    def test_create_department(self):
        response = self.client.post(self.url, content_type=CONTENT_TYPE, data=self.data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        Department.objects.get()

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
