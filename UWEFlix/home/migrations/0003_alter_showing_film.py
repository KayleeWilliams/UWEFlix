# Generated by Django 4.1.5 on 2023-01-02 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_showing"),
    ]

    operations = [
        migrations.AlterField(
            model_name="showing",
            name="film",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="showings",
                to="home.film",
            ),
        ),
    ]
