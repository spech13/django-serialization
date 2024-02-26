from http import HTTPStatus

from django.test import TestCase

from serialization_app.serializers import STORE_MANAGER_NUMBER_PATTERN
from serialization_app.tests.factories import StoreFactory

CONTENT_TYPE = "application/json"


class PartialsUpdateStoreViewTestCase(TestCase):
    url = "/serialization/stores/{id}/partial-update"

    def setUp(self):
        self.store = StoreFactory()
        self.data = {
            "manager_number": "+7 893-398-12-98",
        }

    def test_update_store(self):
        response = self.client.patch(
            self.url.format(id=self.store.id),
            data=self.data,
            content_type=CONTENT_TYPE,
        )
        self.store.refresh_from_db()

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertDictEqual(
            self.data,
            {
                "manager_number": self.store.manager_number,
            },
        )

    def test_forbinded_method(self):
        response = self.client.get(self.url.format(id=self.store.id))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": "Method GET is forbinded"}
        )

    def test_decode_data_error(self):
        data = "some data"
        response = self.client.patch(
            self.url.format(id=self.store.id), data=data, content_type=CONTENT_TYPE
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": f"Json decode error for {data}"}
        )

    def test_no_valid_manager_number(self):
        self.data["manager_number"] = "8 893-398-12-98"

        response = self.client.patch(
            self.url.format(id=self.store.id),
            data=self.data,
            content_type=CONTENT_TYPE,
        )

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
