from django.test import TestCase

from serialization_app.tests.factories import ProductFactory
from serialization_app.tests.get_object_view import GetObjectsView


class GetProductsViewTestCase(GetObjectsView, TestCase):
    url = "/serialization/products/get"
    fields = ["name", "category", "price", "vendor_code", "store_id"]
    factory_class = ProductFactory
