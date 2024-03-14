from django.test import TestCase

from serialization_app.tests.factories import UserFactory
from serialization_app.tests.get_object_view import GetObjectsView


class GetUsersViewTestCase(GetObjectsView, TestCase):
    url = "/serialization/users/get"
    fields = ["id", "name", "created_at", "updated_at"]
    factory_class = UserFactory

    def setUp(self):
        super().setUp()

        for expected_data in self.expected_result:
            expected_data["created_at"] = (
                expected_data["created_at"].isoformat().replace("+00:00", "") + "Z"
            )
            expected_data["updated_at"] = (
                expected_data["updated_at"].isoformat().replace("+00:00", "") + "Z"
            )
