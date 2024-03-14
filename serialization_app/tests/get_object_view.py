# pylint: disable=not-callable
# pylint: disable=no-member

from http import HTTPStatus

CONTENT_TYPE = "application/json"


class GetObjectView:
    url = None
    factory_class = None
    fields = None

    def setUp(self):
        self.getting_object = self.factory_class()

        # pylint: disable=not-an-iterable
        self.expected_result = {
            field_name: getattr(self.getting_object, field_name)
            for field_name in self.fields
        }

    def test_get_object(self):
        response = self.client.get(
            self.url.format(id=self.getting_object.id), content_type=CONTENT_TYPE
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        
        response_json = response.json()
        real_result = {field_name: response_json[field_name] for field_name in self.expected_result}
        self.assertDictEqual(real_result, self.expected_result)

    def test_object_does_not_exist(self):
        response = self.client.get(
            self.url.format(id="other_id"), content_type=CONTENT_TYPE
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_forbinded_method(self):
        response = self.client.post(self.url.format(id=self.getting_object.id))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": "Method POST is forbinded"}
        )
