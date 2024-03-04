from django.test import TestCase

from serialization_app.tests.factories import UserFactory
from serialization_app.tests.get_objects_view import GetObjectsView


class GetUsersViewTestCase(GetObjectsView, TestCase):
    url = "/serialization/users/get"

    def setUp(self):
        self.expected_result = [
            {
                "id": user.id,
                "name": user.name,
                "created_at": user.created_at.isoformat().replace("+00:00", "") + "Z",
                "updated_at": user.updated_at.isoformat().replace("+00:00", "") + "Z",
            }
            for user in UserFactory.create_batch(3)
        ]
