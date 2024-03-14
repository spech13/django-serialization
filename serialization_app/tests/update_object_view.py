# pylint: disable=not-callable
# pylint: disable=no-member

from http import HTTPStatus

CONTENT_TYPE = "application/json"


class UpdateObjectView:
    url = None
    data = None
    factory_class = None

    def setUp(self):
        self.updating_object = self.factory_class()

    def get_and_update_data(self, addition_data):
        data = self.data.copy()
        data.update(addition_data)

        return data

    def test_update_object(self):
        response = self.client.patch(
            self.url.format(id=self.updating_object.id),
            content_type=CONTENT_TYPE,
            data=self.data,
        )
        self.updating_object.refresh_from_db()

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertDictEqual(
            self.data,
            {
                field_name: getattr(self.updating_object, field_name)
                for field_name in self.data.keys()
            },
        )

    def test_forbinded_method(self):
        response = self.client.get(self.url.format(id=self.updating_object.id))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": "Method GET is forbinded"}
        )

    def test_decode_data_error(self):
        data = "some data"
        response = self.client.patch(
            self.url.format(id=self.updating_object.id),
            data=data,
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": f"Json decode error for {data}"}
        )

class UpdateObjectsView:
    def setUp(self):
        self.updated_objects = self.factory_class.create_batch(3)
        for data_item, updated_object in zip(self.data, self.updated_objects):
            data_item["id"] = updated_object.id

    def test_update_object(self):
        response = self.client.patch(
            self.url,
            content_type=CONTENT_TYPE,
            data=self.data,
        )

        for updated_object in self.updated_objects:
            updated_object.refresh_from_db()

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

        result = [
            {
                field_name: getattr(updated_object, field_name)
                for data_item in self.data
                for field_name in data_item
            }
            for updated_object in self.updated_objects
        ]

        for object_data in self.data:
            self.assertTrue(object_data in result)
    
    def test_forbinded_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": "Method GET is forbinded"}
        )

    def test_decode_data_error(self):
        data = "some data"
        response = self.client.patch(
            self.url,
            data=data,
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": f"Json decode error for {data}"}
        )
