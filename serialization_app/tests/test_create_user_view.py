from django.test import TestCase

from serialization_app.models import User
from serialization_app.tests.create_object_view import CreateObjectView


class CreateUserViewTestCase(CreateObjectView, TestCase):
    url = "/serialization/users/create"
    model_class = User
    data = {
        "name": "department-name",
        "password": "password-PaSsWorD",
    }
