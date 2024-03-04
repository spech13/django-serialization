# # pylint: disable=no-member

from http import HTTPStatus

CONTENT_TYPE = "application/json"


class GetObjectsView:
    url = None
    expected_result = None

    def test_get_objects(self):
        response = self.client.get(self.url, content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertListEqual(response.json(), self.expected_result)

    def test_forbinded_method(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": "Method POST is forbinded"}
        )
