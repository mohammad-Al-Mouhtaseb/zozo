# Generated by Django 5.0.4 on 2024-07-06 19:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("to_do_list", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="to_do",
            name="is_done",
        ),
    ]
