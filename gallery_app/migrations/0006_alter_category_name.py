# Generated by Django 4.2.2 on 2023-06-14 15:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gallery_app", "0005_merge_20230614_1817"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                choices=[
                    ("Painting", "Painting"),
                    ("Photography", "Photography"),
                    ("Sculpture", "Sculpture"),
                    ("Prints", "Prints"),
                    ("Work on paper", "Work on paper"),
                    ("Design", "Design"),
                    ("Graphic design", "Graphic design"),
                    ("Collages", "Collages"),
                    ("Illustration", "Illustration"),
                ],
                max_length=255,
                unique=True,
            ),
        ),
    ]