from django.test import TestCase

from serialization_app.models import Book
from serialization_app.tests.create_object_view import CreateObjectsView


class CreateBooksViewTestCase(CreateObjectsView, TestCase):
    url = "/serialization/books/create/many"
    model_class = Book
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
