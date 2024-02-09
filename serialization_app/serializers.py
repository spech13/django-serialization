import re

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from serialization_app.models import HexNut, WorkStation

WORK_STATION_NAME_PATTERN = r"WS-[0-9]{4}$"
WORK_STATION_IP_ADDRESS_PATTERN = r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"
WORK_STATION_SERIAL_NUMBER_PATTERN = r"^[A-Z]{4}-[A-Z]{4}-[A-Z]{4}-[A-Z]{4}$"


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
        if len(value) > 7:
            raise serializers.ValidationError(
                "length of name field must not exceed 7 characters"
            )

        if not re.match(WORK_STATION_NAME_PATTERN, value):
            raise serializers.ValidationError(
                "name field must match the pattern "
                f"{WORK_STATION_NAME_PATTERN}. Example WS-1296"
            )

        return value

    def validate_serial_number(self, value):
        if len(value) > 19:
            raise serializers.ValidationError(
                "length of serial_number field must not exceed 15 characters"
            )

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
