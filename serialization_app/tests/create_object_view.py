# pylint: disable=no-member
# pylint: disable=not-an-iterable

from http import HTTPStatus

from serialization_app.tests.base_object_view import BaseObjectView

CONTENT_TYPE = "application/json"


class BaseCreateObjectView(BaseObjectView):
    model_class = None

    def test_decode_data_error(self):
        data = "some data"
        response = self.client.post(self.url, data=data, content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": f"Json decode error for {data}"}
        )


class CreateObjectView(BaseCreateObjectView):
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


class CreateObjectsView(BaseCreateObjectView):
    def test_create_objects(self):
        response = self.client.post(self.url, content_type=CONTENT_TYPE, data=self.data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        created_objects = self.model_class.objects.all()
        result = [
            {
                field_name: getattr(created_object, field_name)
                for data_item in self.data
                for field_name in data_item
            }
            for created_object in created_objects
        ]
        for object_data in self.data:
            self.assertTrue(object_data in result)
