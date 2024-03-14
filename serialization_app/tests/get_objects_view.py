# # pylint: disable=no-member

from http import HTTPStatus

CONTENT_TYPE = "application/json"


class GetObjectsView:
    url = None
    expected_result = None

    def test_get_objects(self):
        response = self.client.get(self.url, content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response_json = response.json()
        real_result = [{field_name: real_data[field_name] for field_name in expected_data} for expected_data, real_data in zip(self.expected_result, response_json)]
        self.assertListEqual(real_result, self.expected_result)

    def test_forbinded_method(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": "Method POST is forbinded"}
        )
