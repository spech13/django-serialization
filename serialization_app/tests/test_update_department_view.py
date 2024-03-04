from django.test import TestCase

from serialization_app.tests.factories import DepartmentFactory
from serialization_app.tests.update_object_view import UpdateObjectView


class UpdateDepartmentViewTestCase(UpdateObjectView, TestCase):
    url = "/serialization/departments/{id}/update"
    factory_class = DepartmentFactory
    data = {
        "name": "department-name",
        "employees_number": 10,
        "description": "department-description",
    }
