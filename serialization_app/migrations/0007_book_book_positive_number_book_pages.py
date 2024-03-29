# Generated by Django 5.0.1 on 2024-03-14 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("serialization_app", "0006_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
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
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                ("author", models.CharField(max_length=255, verbose_name="Author")),
                ("number_book_pages", models.IntegerField()),
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
            model_name="book",
            constraint=models.CheckConstraint(
                check=models.Q(("number_book_pages__gte", 0)),
                name="positive_number_book_pages",
            ),
        ),
    ]
