from http import HTTPStatus

from django.test import TestCase

from serialization_app.models import Store
from serialization_app.serializers import STORE_MANAGER_NUMBER_PATTERN

CONTENT_TYPE = "application/json"


class CreateStoreViewTestCase(TestCase):
    url = "/serialization/stores/create"

    def setUp(self):
        self.data = {
            "address": "Moscow, Petrovskaya 16",
            "manager_name": "Ivan Sokolov",
            "manager_number": "+7 893-398-12-98",
        }

    def test_create_store(self):
        response = self.client.post(self.url, data=self.data, content_type=CONTENT_TYPE)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        Store.objects.get()

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

    def test_no_valid_manager_number(self):
        self.data["manager_number"] = "8 893-398-12-98"

        response = self.client.post(self.url, data=self.data, content_type=CONTENT_TYPE)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "validation_errors": {
                    "manager_number": "manger number must match "
                    f"the pattern {STORE_MANAGER_NUMBER_PATTERN}"
                }
            },
        )
