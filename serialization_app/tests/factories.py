# pylint: disable=consider-using-f-string
from factory import Sequence
from factory.django import DjangoModelFactory

from serialization_app.models import HexNut, WorkStation


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
