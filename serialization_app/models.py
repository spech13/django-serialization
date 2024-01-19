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
