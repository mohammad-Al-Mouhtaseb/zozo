# Generated by Django 5.0.4 on 2024-07-02 08:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="private_key",
            field=models.TextField(blank=True, default="", max_length=1200, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="public_key",
            field=models.TextField(blank=True, default="", max_length=1200, null=True),
        ),
    ]
