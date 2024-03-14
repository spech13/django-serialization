# pylint: disable=no-member

from http import HTTPStatus


class BaseObjectView:
    url = None
    data = None

    def get_and_update_data(self, addition_data):
        data = self.data.copy()
        data.update(addition_data)

        return data

    def test_forbinded_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": "Method GET is forbinded"}
        )
