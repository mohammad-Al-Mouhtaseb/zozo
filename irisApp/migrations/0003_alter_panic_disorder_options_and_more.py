# Generated by Django 5.0.4 on 2024-04-05 12:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("irisApp", "0002_alter_panic_disorder_person_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="panic_disorder",
            options={"verbose_name": "Panic_Disorder"},
        ),
        migrations.RenameField(
            model_name="panic_disorder",
            old_name="Doctor_Id",
            new_name="Doctor_email",
        ),
        migrations.RenameField(
            model_name="panic_disorder",
            old_name="Person_Id",
            new_name="Person_email",
        ),
    ]