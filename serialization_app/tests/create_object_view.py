# pylint: disable=no-member

from http import HTTPStatus

CONTENT_TYPE = "application/json"


class CreateObjectView:
    url = None
    model_class = None
    data = None

    def get_and_update_data(self, addition_data):
        data = self.data.copy()
        data.update(addition_data)

        return data

    def test_create_object(self):
        response = self.client.post(self.url, content_type=CONTENT_TYPE, data=self.data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        created_object = self.model_class.objects.get()
        self.assertDictEqual(
            self.data,
            {
                field_name: getattr(created_object, field_name)
                for field_name in self.data.keys()
            },
        )

    def test_forbinded_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": "Method GET is forbinded"}
        )

    def test_decode_data_error(self):
        data = "some data"
        response = self.client.post(self.url, data=data, content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": f"Json decode error for {data}"}
        )
