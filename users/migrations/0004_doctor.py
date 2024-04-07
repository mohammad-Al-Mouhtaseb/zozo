# Generated by Django 5.0.4 on 2024-04-05 07:25

import django.db.models.deletion
import users.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_patient"),
    ]

    operations = [
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "clinic_address",
                    models.CharField(blank=True, default="", max_length=50, null=True),
                ),
                (
                    "rate",
                    models.DecimalField(
                        blank=True,
                        decimal_places=1,
                        default=0.0,
                        max_digits=2,
                        null=True,
                    ),
                ),
                (
                    "num_of_rate",
                    models.DecimalField(
                        blank=True,
                        decimal_places=1,
                        default=0.0,
                        max_digits=5,
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("users.user",),
            managers=[
                ("objects", users.models.CustomUserManager()),
            ],
        ),
    ]