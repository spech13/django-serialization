from http import HTTPStatus

from django.test import TestCase

from serialization_app.models import Product
from serialization_app.serializers import PRODUCT_VENDOR_CODE_PATTERN
from serialization_app.tests.create_object_view import CONTENT_TYPE, CreateObjectView
from serialization_app.tests.factories import StoreFactory


class CreateProductViewTestCase(CreateObjectView, TestCase):
    url = "/serialization/products/create"
    model_class = Product

    def setUp(self):
        self.data = {
            "name": "product-name",
            "category": Product.FURNITURE,
            "price": 12.6,
            "vendor_code": "JKKD-DKJF-SKJD-KSLD",
            "store_id": StoreFactory().id,
        }

    def test_no_valid_vendor_code(self):
        data = self.get_and_update_data({"vendor_code": "vendor-code"})

        response = self.client.post(self.url, content_type=CONTENT_TYPE, data=data)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "validation_errors": {
                    "vendor_code": "vendor_code must match "
                    f"the pattern {PRODUCT_VENDOR_CODE_PATTERN}"
                }
            },
        )

        data["vendor_code"] = "very-long-vendor-code"
        response = self.client.post(self.url, content_type=CONTENT_TYPE, data=data)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "validation_errors": {
                    "vendor_code": "Ensure this field has no more than 19 characters."
                }
            },
        )

    def test_no_valid_category(self):
        response = self.client.post(
            self.url,
            content_type=CONTENT_TYPE,
            data=self.get_and_update_data({"category": "no-valid-category"}),
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "validation_errors": {
                    "category": '"no-valid-category" is not a valid choice.'
                }
            },
        )
