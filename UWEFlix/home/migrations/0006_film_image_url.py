# Generated by Django 4.1.5 on 2023-01-03 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0005_film_imdb"),
    ]

    operations = [
        migrations.AddField(
            model_name="film",
            name="image_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]