# Generated by Django 5.1.3 on 2024-11-29 21:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resources", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="venuebooking",
            name="venue",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bookings",
                to="resources.venue",
            ),
        ),
    ]