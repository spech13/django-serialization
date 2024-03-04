from django.test import TestCase

from serialization_app.tests.factories import ProductFactory
from serialization_app.tests.get_objects_view import GetObjectsView


class GetProductsViewTestCase(GetObjectsView, TestCase):
    url = "/serialization/products/get"

    def setUp(self):
        self.expected_result = [
            {
                "name": product.name,
                "category": product.category,
                "price": product.price,
                "vendor_code": product.vendor_code,
                "store_id": product.store.id,
            }
            for product in ProductFactory.create_batch(3)
        ]
