from django.test import TestCase

from serialization_app.models import Department
from serialization_app.tests.create_object_view import CreateObjectView


class CreateDepartentViewTestCase(CreateObjectView, TestCase):
    url = "/serialization/departments/create"
    model_class = Department
    data = {
        "name": "department-name",
        "employees_number": 10,
        "description": "department-description",
    }
