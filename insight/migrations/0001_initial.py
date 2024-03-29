# Generated by Django 5.0.3 on 2024-03-07 16:24

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserImageCase",
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
                ("image", models.ImageField(upload_to="")),
                ("userPrompt", models.TextField()),
                ("resultPrompt", models.TextField()),
            ],
        ),
    ]
