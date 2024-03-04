from django.test import TestCase

from serialization_app.tests.factories import ProductFactory
from serialization_app.tests.get_object_view import GetObjectView


class GetProductViewTestCase(GetObjectView, TestCase):
    url = "/serialization/products/{id}/get"
    fields = ["name", "category", "price", "vendor_code", "store_id"]
    factory_class = ProductFactory
