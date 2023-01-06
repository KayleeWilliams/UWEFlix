# Generated by Django 4.1.5 on 2023-01-06 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0006_film_image_url"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ticket",
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
                ("name", models.CharField(max_length=100)),
                ("price", models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
