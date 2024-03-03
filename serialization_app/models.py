from django.db import models
from django.db.models import CheckConstraint, Q


class HexNut(models.Model):
    designation = models.CharField(
        verbose_name="Designation", max_length=255, unique=True
    )
    large_thread_pitch = models.FloatField(verbose_name="Large thread pitch")
    small_thread_pitch = models.FloatField(
        verbose_name="Small thread pitch", null=True, blank=True
    )
    size = models.FloatField(verbose_name="Size")
    hight = models.FloatField(verbose_name="Hight")
    e = models.FloatField(verbose_name="e")
    mass_1000_pc = models.FloatField(verbose_name="Mass in 1000 pc., kg")
    amout_pc_in_kg = models.FloatField(verbose_name="Amount pc. in 1 kg")
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    def __str__(self):
        return self.designation

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(large_thread_pitch__gte=0.0),
                name="hex_nut_large_thread_pitch_min_value",
            ),
            CheckConstraint(
                check=Q(small_thread_pitch__gte=0.0),
                name="hex_nut_small_thread_pitch_min_value",
            ),
            CheckConstraint(check=Q(size__gte=0.0), name="hex_nut_size_min_value"),
            CheckConstraint(check=Q(hight__gte=0.0), name="hex_nut_hight_min_value"),
            CheckConstraint(check=Q(e__gte=0.0), name="hex_nut_e_min_value"),
            CheckConstraint(
                check=Q(mass_1000_pc__gte=0.0), name="hex_nut_mass_1000_pc_min_value"
            ),
            CheckConstraint(
                check=Q(amout_pc_in_kg__gte=0.0),
                name="hex_nut_amout_pc_in_kg_min_value",
            ),
        ]


class WorkStation(models.Model):
    name = models.CharField(verbose_name="Name", max_length=7, unique=True)
    ip_address = models.CharField(verbose_name="Ip address", max_length=15, unique=True)
    disk_capacity = models.FloatField(verbose_name="Disk capacity GiB")
    ram = models.FloatField(verbose_name="RAM GiB")
    cpu = models.FloatField(verbose_name="CPU GiB")
    serial_number = models.CharField(
        verbose_name="Serial Number", max_length=19, unique=True
    )
    employee_name = models.CharField(
        verbose_name="Employee name", max_length=255, null=True, blank=True
    )
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    address = models.CharField(verbose_name="Address", max_length=255, unique=True)
    manager_name = models.CharField(
        verbose_name="Manager name", max_length=255, null=True, blank=True
    )
    manager_number = models.CharField(
        verbose_name="Manager number", max_length=16, null=True, blank=True
    )

    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    def __str__(self):
        return self.address


class Product(models.Model):
    FURNITURE = "FURNITURE"
    TOOL = "TOOL"
    HOUSEHOLD_APPLIANCE = "HOUSEHOLD-APPLIANCE"

    CATEGORIES = (
        (FURNITURE, FURNITURE),
        (TOOL, TOOL),
        (HOUSEHOLD_APPLIANCE, HOUSEHOLD_APPLIANCE),
    )

    name = models.CharField(verbose_name="Name", max_length=255, unique=True)
    category = models.CharField(
        verbose_name="Category", max_length=255, choices=CATEGORIES
    )
    price = models.FloatField(verbose_name="Price", default=0)
    vendor_code = models.CharField(
        verbose_name="Vendor code", max_length=19, unique=True
    )
    store = models.ForeignKey(
        Store, verbose_name="Store", on_delete=models.CASCADE, related_name="products"
    )

    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(verbose_name="Name", max_length=255, unique=True)
    employees_number = models.SmallIntegerField(verbose_name="Employees number")
    description = models.CharField(
        verbose_name="Description", max_length=255, null=True, blank=True
    )

    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    @classmethod
    def get_default_id(cls):
        department, new = cls.objects.get_or_create(
            name="Free",
            defaults={"employees_number": 0, "description": "Free employee"},
        )
        return (department or new).id

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(verbose_name="First name", max_length=255)
    last_name = models.CharField(verbose_name="Last name", max_length=255)
    age = models.SmallIntegerField(verbose_name="Age")

    department = models.ForeignKey(
        Department,
        verbose_name="Department",
        on_delete=models.SET_DEFAULT,
        related_name="employees",
        default=Department.get_default_id,
    )

    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
