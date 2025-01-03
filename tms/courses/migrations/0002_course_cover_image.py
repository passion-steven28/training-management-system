# Generated by Django 5.1.3 on 2024-11-29 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="cover_image",
            field=models.ImageField(
                blank=True,
                default="course_covers/default.jpg",
                null=True,
                upload_to="course_covers/",
            ),
        ),
    ]
