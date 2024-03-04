from django.test import TestCase

from serialization_app.tests.factories import UserFactory
from serialization_app.tests.update_object_view import UpdateObjectView


class UpdateUserViewTestCase(UpdateObjectView, TestCase):
    url = "/serialization/users/{id}/update"
    factory_class = UserFactory
    data = {
        "name": "department-name",
        "password": "password-PaSsWorD",
    }
