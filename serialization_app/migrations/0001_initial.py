# Generated by Django 5.0.1 on 2024-01-21 09:44

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HexNut",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "designation",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Designation"
                    ),
                ),
                (
                    "large_thread_pitch",
                    models.FloatField(verbose_name="Large thread pitch"),
                ),
                (
                    "small_thread_pitch",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Small thread pitch"
                    ),
                ),
                ("size", models.FloatField(verbose_name="Size")),
                ("hight", models.FloatField(verbose_name="Hight")),
                ("e", models.FloatField(verbose_name="e")),
                (
                    "mass_1000_pc",
                    models.FloatField(verbose_name="Mass in 1000 pc., kg"),
                ),
                (
                    "amout_pc_in_kg",
                    models.FloatField(verbose_name="Amount pc. in 1 kg"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="hexnut",
            constraint=models.CheckConstraint(
                check=models.Q(("large_thread_pitch__gte", 0.0)),
                name="hex_nut_large_thread_pitch_min_value",
            ),
        ),
        migrations.AddConstraint(
            model_name="hexnut",
            constraint=models.CheckConstraint(
                check=models.Q(("small_thread_pitch", 0.0)),
                name="hex_nut_small_thread_pitch_min_value",
            ),
        ),
        migrations.AddConstraint(
            model_name="hexnut",
            constraint=models.CheckConstraint(
                check=models.Q(("size", 0.0)), name="hex_nut_size_min_value"
            ),
        ),
        migrations.AddConstraint(
            model_name="hexnut",
            constraint=models.CheckConstraint(
                check=models.Q(("hight", 0.0)), name="hex_nut_hight_min_value"
            ),
        ),
        migrations.AddConstraint(
            model_name="hexnut",
            constraint=models.CheckConstraint(
                check=models.Q(("e", 0.0)), name="hex_nut_e_min_value"
            ),
        ),
        migrations.AddConstraint(
            model_name="hexnut",
            constraint=models.CheckConstraint(
                check=models.Q(("mass_1000_pc", 0.0)),
                name="hex_nut_mass_1000_pc_min_value",
            ),
        ),
        migrations.AddConstraint(
            model_name="hexnut",
            constraint=models.CheckConstraint(
                check=models.Q(("amout_pc_in_kg", 0.0)),
                name="hex_nut_amout_pc_in_kg_min_value",
            ),
        ),
    ]