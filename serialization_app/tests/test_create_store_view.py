from http import HTTPStatus

from django.test import TestCase

from serialization_app.models import Store
from serialization_app.serializers import STORE_MANAGER_NUMBER_PATTERN
from serialization_app.tests.create_object_view import CONTENT_TYPE, CreateObjectView


class CreateStoreViewTestCase(CreateObjectView, TestCase):
    url = "/serialization/stores/create"
    model_class = Store
    data = {
        "address": "Moscow, Petrovskaya 16",
        "manager_name": "Ivan Sokolov",
        "manager_number": "+7 893-398-12-98",
    }

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
