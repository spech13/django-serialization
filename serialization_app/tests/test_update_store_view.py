from http import HTTPStatus

from django.test import TestCase

from serialization_app.serializers import STORE_MANAGER_NUMBER_PATTERN
from serialization_app.tests.factories import StoreFactory
from serialization_app.tests.update_object_view import CONTENT_TYPE, UpdateObjectView


class UpdateStoreViewTestCase(UpdateObjectView, TestCase):
    url = "/serialization/stores/{id}/update"
    factory_class = StoreFactory
    data = {
        "address": "Moscow, Petrovskaya 16",
        "manager_name": "Ivan Sokolov",
        "manager_number": "+7 893-398-12-98",
    }

    def test_no_valid_manager_number(self):
        response = self.client.patch(
            self.url.format(id=StoreFactory().id),
            data=self.get_and_update_data({"manager_number": "8 893-398-12-98"}),
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
