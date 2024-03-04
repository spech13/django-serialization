from django.test import TestCase

from serialization_app.tests.factories import StoreFactory
from serialization_app.tests.get_object_view import GetObjectView


class GetStoreViewTestCase(GetObjectView, TestCase):
    url = "/serialization/stores/{id}/get"
    fields = ["address", "manager_name", "manager_number"]
    factory_class = StoreFactory
