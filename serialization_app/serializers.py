from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from serialization_app.models import HexNut


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
