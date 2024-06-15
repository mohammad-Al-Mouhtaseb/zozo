# Generated by Django 5.0.4 on 2024-06-14 07:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("irisApp", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="iris",
            name="Durable_Asset_Category",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AddField(
            model_name="iris",
            name="Education_Level",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AddField(
            model_name="iris",
            name="Lasting_Investment_Category",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AddField(
            model_name="iris",
            name="Living_Expenses_Category",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AddField(
            model_name="iris",
            name="Married",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AddField(
            model_name="iris",
            name="No_Lasting_Investment_Category",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AddField(
            model_name="iris",
            name="Number_Children",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AddField(
            model_name="iris",
            name="Other_Expenses_Category",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AddField(
            model_name="iris",
            name="Save_Asset_Category",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AddField(
            model_name="iris",
            name="depressed",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AddField(
            model_name="iris",
            name="gained_asset_Category",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AddField(
            model_name="iris",
            name="incoming_business",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AddField(
            model_name="iris",
            name="incoming_no_business",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AddField(
            model_name="iris",
            name="incoming_salary",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AddField(
            model_name="iris",
            name="labor_primary",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AddField(
            model_name="iris",
            name="total_members",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
    ]