from django.test import TestCase

from serialization_app.models import Book
from serialization_app.tests.create_object_view import CreateObjectView


class CreateBookViewTestCase(CreateObjectView, TestCase):
    url = "/serialization/books/create"
    model_class = Book
    data = {
        "title": "book-title",
        "author": "book-author",
        "number_book_pages": 300,
    }
