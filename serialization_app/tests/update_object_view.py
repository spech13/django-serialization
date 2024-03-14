# pylint: disable=not-callable
# pylint: disable=no-member
# pylint: disable=not-an-iterable

from http import HTTPStatus

from serialization_app.tests.base_object_view import BaseObjectView

CONTENT_TYPE = "application/json"


class BaseUpdateObjectView(BaseObjectView):
    factory_class = None

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


class UpdateObjectView(BaseUpdateObjectView):
    def setUp(self):
        self.updated_object = self.factory_class()
        self.object_does_not_exist_url = self.url.format(id="other-url")
        self.url = self.url.format(id=self.updated_object.id)

    def test_update_object(self):
        response = self.client.patch(
            self.url,
            content_type=CONTENT_TYPE,
            data=self.data,
        )
        self.updated_object.refresh_from_db()

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertDictEqual(
            self.data,
            {
                field_name: getattr(self.updated_object, field_name)
                for field_name in self.data.keys()
            },
        )

    def test_object_does_not_exist(self):
        response = self.client.patch(
            self.object_does_not_exist_url, content_type=CONTENT_TYPE
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class UpdateObjectsView(BaseUpdateObjectView):
    def setUp(self):
        self.updated_objects = self.factory_class.create_batch(3)
        for data_item, updated_object in zip(self.data, self.updated_objects):
            data_item["id"] = updated_object.id

    def test_update_objects(self):
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
