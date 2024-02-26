from http import HTTPStatus

from django.test import TestCase

from serialization_app.models import Product
from serialization_app.serializers import PRODUCT_VENDOR_CODE_PATTERN
from serialization_app.tests.factories import ProductFactory, StoreFactory

CONTENT_TYPE = "application/json"


class UpdateProductViewTestCase(TestCase):
    url = "/serialization/products/{id}/update"

    def setUp(self):
        self.store = StoreFactory()
        self.product = ProductFactory()
        self.data = {
            "name": "product-name",
            "category": Product.FURNITURE,
            "price": 12.6,
            "vendor_code": "JKKD-DKJF-SKJD-KSLD",
            "store_id": self.store.id,
        }

    def test_update_product(self):
        response = self.client.patch(
            self.url.format(id=self.product.id),
            content_type=CONTENT_TYPE,
            data=self.data,
        )
        self.product.refresh_from_db()

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertDictEqual(
            self.data,
            {
                "name": self.product.name,
                "category": self.product.category,
                "price": self.product.price,
                "vendor_code": self.product.vendor_code,
                "store_id": self.product.store.id,
            },
        )

    def test_forbinded_method(self):
        response = self.client.get(self.url.format(id=self.product.id))

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": "Method GET is forbinded"}
        )

    def test_decode_data_error(self):
        self.data = "some data"
        response = self.client.patch(
            self.url.format(id=self.product.id),
            content_type=CONTENT_TYPE,
            data=self.data,
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error_message": f"Json decode error for {self.data}"}
        )

    def test_no_valid_vendor_code(self):
        self.data["vendor_code"] = "vendor-code"
        response = self.client.patch(
            self.url.format(id=self.product.id),
            content_type=CONTENT_TYPE,
            data=self.data,
        )

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

        self.data["vendor_code"] = "very-long-vendor-code"
        response = self.client.patch(
            self.url.format(id=self.product.id),
            content_type=CONTENT_TYPE,
            data=self.data,
        )

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
        self.data["category"] = "no-valid-category"
        response = self.client.patch(
            self.url.format(id=self.product.id),
            content_type=CONTENT_TYPE,
            data=self.data,
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
