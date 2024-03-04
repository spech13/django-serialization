from django.test import TestCase

from serialization_app.tests.factories import UserFactory
from serialization_app.tests.get_object_view import GetObjectView

CONTENT_TYPE = "application/json"


class GetUserViewTestCase(GetObjectView, TestCase):
    url = "/serialization/users/{id}/get"
    fields = ["id", "name", "created_at", "updated_at"]
    factory_class = UserFactory

    def setUp(self):
        super().setUp()

        self.expected_result["created_at"] = (
            self.expected_result["created_at"].isoformat().replace("+00:00", "") + "Z"
        )
        self.expected_result["updated_at"] = (
            self.expected_result["updated_at"].isoformat().replace("+00:00", "") + "Z"
        )
