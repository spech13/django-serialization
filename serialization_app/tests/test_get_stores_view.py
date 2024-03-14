from django.test import TestCase

from serialization_app.tests.factories import StoreFactory
from serialization_app.tests.get_object_view import GetObjectsView


class GetStoresViewTestCase(GetObjectsView, TestCase):
    url = "/serialization/stores/get"
    fields = ["address", "manager_name", "manager_number"]
    factory_class = StoreFactory
