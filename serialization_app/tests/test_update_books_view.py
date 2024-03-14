from django.test import TestCase

from serialization_app.tests.factories import BookFactory
from serialization_app.tests.update_object_view import UpdateObjectsView


class UpdateBooksViewTestCase(UpdateObjectsView, TestCase):
    url = "/serialization/books/update/many"
    factory_class = BookFactory
    data = [
        {
            "title": "my-book-title-1",
            "author": "my-book-author-1",
            "number_book_pages": 300,
        },
        {
            "title": "my-book-title-2",
            "author": "my-book-author-2",
            "number_book_pages": 300,
        },
    ]
