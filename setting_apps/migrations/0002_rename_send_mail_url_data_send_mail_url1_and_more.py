# Generated by Django 5.0.4 on 2024-06-15 16:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("setting_apps", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="data",
            old_name="Send_Mail_URL",
            new_name="Send_Mail_URL1",
        ),
        migrations.AddField(
            model_name="data",
            name="Send_Mail_URL2",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
