# Generated by Django 4.1.5 on 2023-01-06 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0008_remove_booking_seats_tickettypequantity_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="film",
            name="backdrop_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
