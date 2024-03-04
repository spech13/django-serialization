from django.test import TestCase

from serialization_app.tests.factories import StoreFactory
from serialization_app.tests.get_objects_view import GetObjectsView


class GetStoresViewTestCase(GetObjectsView, TestCase):
    url = "/serialization/stores/get"

    def setUp(self):
        self.expected_result = [
            {
                "address": store.address,
                "manager_name": store.manager_name,
                "manager_number": store.manager_number,
            }
            for store in StoreFactory.create_batch(3)
        ]
