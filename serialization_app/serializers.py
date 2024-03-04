import re

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from serialization_app.models import (
    Department,
    Employee,
    HexNut,
    Product,
    Store,
    User,
    WorkStation,
)

WORK_STATION_NAME_PATTERN = r"WS-[0-9]{4}$"
WORK_STATION_IP_ADDRESS_PATTERN = r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"
WORK_STATION_SERIAL_NUMBER_PATTERN = r"^[A-Z]{4}-[A-Z]{4}-[A-Z]{4}-[A-Z]{4}$"
STORE_MANAGER_NUMBER_PATTERN = r"^\+7 [0-9]{3}-[0-9]{3}-[0-9]{2}-[0-9]{2}$"
PRODUCT_VENDOR_CODE_PATTERN = r"^[A-Z]{4}-[A-Z]{4}-[A-Z]{4}-[A-Z]{4}$"


class HexNutSerializer(serializers.Serializer):
    designation = serializers.CharField(max_length=255)
    large_thread_pitch = serializers.FloatField(min_value=0.0)
    small_thread_pitch = serializers.FloatField(required=False, min_value=0.0)
    size = serializers.FloatField(min_value=0.0)
    hight = serializers.FloatField(min_value=0.0)
    e = serializers.FloatField(min_value=0.0)
    mass_1000_pc = serializers.FloatField(min_value=0.0)
    amout_pc_in_kg = serializers.FloatField(min_value=0.0)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=HexNut.objects.all(), fields=["designation"]
            )
        ]

    def create(self, validated_data):
        return HexNut.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.designation = validated_data.get("designation")
        instance.large_thread_pitch = validated_data.get("large_thread_pitch")
        instance.small_thread_pitch = validated_data.get("small_thread_pitch")
        instance.size = validated_data.get("size")
        instance.hight = validated_data.get("hight")
        instance.e = validated_data.get("e")
        instance.mass_1000_pc = validated_data.get("mass_1000_pc")
        instance.amout_pc_in_kg = validated_data.get("amout_pc_in_kg")

        instance.save()
        return instance


def validate_ip_address(value):
    if not re.match(WORK_STATION_IP_ADDRESS_PATTERN, value):
        raise serializers.ValidationError(
            "ip_address field must match "
            f"the pattern {WORK_STATION_IP_ADDRESS_PATTERN}"
        )

    for unit in value.split("."):
        if int(unit) > 255:
            raise serializers.ValidationError(f"number {unit} must be less 255")


class WorkStationSerializer(serializers.ModelSerializer):
    ip_address = serializers.CharField(max_length=15, validators=[validate_ip_address])

    class Meta:
        model = WorkStation
        fields = [
            "id",
            "name",
            "ip_address",
            "disk_capacity",
            "ram",
            "cpu",
            "serial_number",
            "employee_name",
        ]

    def validate_name(self, value):
        if not re.match(WORK_STATION_NAME_PATTERN, value):
            raise serializers.ValidationError(
                "name field must match the pattern "
                f"{WORK_STATION_NAME_PATTERN}. Example WS-1296"
            )

        return value

    def validate_serial_number(self, value):
        if not re.match(WORK_STATION_SERIAL_NUMBER_PATTERN, value):
            raise serializers.ValidationError(
                "serial_number field must match "
                f"the pattern {WORK_STATION_SERIAL_NUMBER_PATTERN}"
            )

        return value

    def validate(self, data):
        if data["cpu"] > data["ram"] or data["ram"] > data["disk_capacity"]:
            raise serializers.ValidationError(
                "validation data must satisfy "
                "the requirement cpu < rum < disck_capacity"
            )

        return data


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["address", "manager_name", "manager_number"]

    def validate_manager_number(self, value):
        if not re.match(STORE_MANAGER_NUMBER_PATTERN, value):
            raise serializers.ValidationError(
                "manger number must match"
                f" the pattern {STORE_MANAGER_NUMBER_PATTERN}"
            )

        return value


class ProductSerializer(serializers.ModelSerializer):
    store_id = serializers.PrimaryKeyRelatedField(
        queryset=Store.objects.all(), source="store"
    )

    class Meta:
        model = Product
        fields = ["name", "category", "price", "vendor_code", "store_id"]

    def validate_vendor_code(self, value):
        if not re.match(PRODUCT_VENDOR_CODE_PATTERN, value):
            raise serializers.ValidationError(
                f"vendor_code must match the pattern {PRODUCT_VENDOR_CODE_PATTERN}"
            )

        return value

    def validate_category(self, value):
        if (value, value) not in Product.CATEGORIES:
            raise serializers.ValidationError(
                f"category must be in {Product.CATEGORIES}"
            )

        return value


class DepartmentSerializer(serializers.Serializer):
    name = serializers.CharField()
    employees_number = serializers.IntegerField()
    description = serializers.CharField()

    def create(self, validated_data):
        return Department.objects.create(**validated_data)

    def update(self, instance, validated_data):
        Department.objects.filter(id=instance.id).update(**validated_data)
        return instance


class EmployeeSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    age = serializers.IntegerField()

    department = DepartmentSerializer(required=False)
    department_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        if validated_data.get("department_id"):
            return Employee.objects.create(
                department=Department.objects.get(
                    id=validated_data.pop("department_id")
                ),
                **validated_data,
            )

        if validated_data.get("department"):
            return Employee.objects.create(
                department=Department.objects.create(
                    **validated_data.pop("department")
                ),
                **validated_data,
            )

        return Employee.objects.create(
            department=Department.objects.get(id=Department.get_default_id()),
            **validated_data,
        )

    def update(self, instance, validated_data):
        Employee.objects.filter(id=instance.id).update(**validated_data)
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}
