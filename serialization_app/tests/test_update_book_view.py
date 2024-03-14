from django.test import TestCase

from serialization_app.tests.factories import BookFactory
from serialization_app.tests.update_object_view import UpdateObjectView


class UpdateBookViewTestCase(UpdateObjectView, TestCase):
    url = "/serialization/books/{id}/update"
    factory_class = BookFactory
    data = {
        "title": "book-title",
        "author": "book-author",
        "number_book_pages": 300,
    }
