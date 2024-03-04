# pylint: disable=consider-using-f-string
from datetime import datetime

from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from serialization_app.models import (
    Department,
    Employee,
    HexNut,
    Product,
    Store,
    User,
    WorkStation,
)


class HexNutFactory(DjangoModelFactory):
    class Meta:
        model = HexNut

    designation = Sequence("hex-nut-{}".format)
    large_thread_pitch = 0.5
    small_thread_pitch = 1
    size = 0.5
    hight = 0.5
    e = 0.5
    mass_1000_pc = 0.5
    amout_pc_in_kg = 0.5


class WorkStationFactory(DjangoModelFactory):
    class Meta:
        model = WorkStation

    name = Sequence("WS-{}".format)
    ip_address = Sequence("192.168.12.{}".format)
    disk_capacity = 10
    ram = 4
    cpu = 2
    serial_number = Sequence("SERI-ALNU-BERS-ERIA-{}".format)
    employee_name = Sequence("employee-name-{}".format)


class StoreFactory(DjangoModelFactory):
    class Meta:
        model = Store

    address = Sequence("store-{}".format)
    manager_name = Sequence("manger-{}".format)
    manager_number = Sequence("manager-number-{}".format)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = Sequence("product-{}".format)
    category = Sequence("category-{}".format)
    price = 12.6
    vendor_code = Sequence("vendor-code-{}".format)
    store = SubFactory(StoreFactory)


class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = Department

    name = Sequence("department-{}".format)
    employees_number = 50
    description = Sequence("desctiption-{}".format)


class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = Employee

    first_name = Sequence("first-name-{}".format)
    last_name = Sequence("last-name-{}".format)
    age = 35
    department = SubFactory(DepartmentFactory)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    name = Sequence("user-name-{}".format)
    password = Sequence("user-password-{}".format)
    created_at = datetime.now()
    updated_at = datetime.now()
