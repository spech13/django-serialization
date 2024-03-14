from django.test import TestCase

from serialization_app.tests.factories import BookFactory
from serialization_app.tests.get_objects_view import GetObjectsView


class GetBookViewTestCase(GetObjectsView, TestCase):
    url = "/serialization/books/get"

    def setUp(self):
        self.expected_result = [
            {
                "title": book.title,
                "author": book.author,
                "number_book_pages": book.number_book_pages,
            }
            for book in BookFactory.create_batch(3)
        ]
