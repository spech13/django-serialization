from django.test import TestCase

from serialization_app.tests.factories import BookFactory
from serialization_app.tests.get_object_view import GetObjectsView


class GetBooksViewTestCase(GetObjectsView, TestCase):
    url = "/serialization/books/get"
    fields = [
        "title",
        "author",
        "number_book_pages",
    ]
    factory_class = BookFactory
