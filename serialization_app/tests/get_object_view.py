# pylint: disable=not-callable
# pylint: disable=no-member
# pylint: disable=not-an-iterable

from http import HTTPStatus

from serialization_app.tests.base_object_view import BaseObjectView

CONTENT_TYPE = "application/json"


class BaseGetObjectView(BaseObjectView):
    fields = None
    factory_class = None

    def test_forbinded_method(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": "Method POST is forbinded"}
        )


class GetObjectView(BaseGetObjectView):
    def setUp(self):
        self.got_object = self.factory_class()

        self.object_does_not_exist_url = self.url.format(id="other-url")
        self.url = self.url.format(id=self.got_object.id)

        self.expected_result = {
            field_name: getattr(self.got_object, field_name)
            for field_name in self.fields
        }

    def test_get_object(self):
        response = self.client.get(self.url, content_type=CONTENT_TYPE)

        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_json = response.json()
        real_result = {
            field_name: response_json[field_name] for field_name in self.expected_result
        }
        self.assertDictEqual(real_result, self.expected_result)

    def test_object_does_not_exist(self):
        response = self.client.get(
            self.object_does_not_exist_url, content_type=CONTENT_TYPE
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class GetObjectsView(BaseGetObjectView):
    def setUp(self):
        self.expected_result = [
            {field_name: getattr(got_object, field_name) for field_name in self.fields}
            for got_object in self.factory_class.create_batch(3)
        ]

    def test_get_objects(self):
        response = self.client.get(self.url, content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        real_result = [
            {field_name: real_data[field_name] for field_name in self.fields}
            for real_data in response.json()
        ]
        self.assertListEqual(real_result, self.expected_result)
