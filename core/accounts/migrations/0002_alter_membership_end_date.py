# Generated by Django 4.2.6 on 2024-01-10 15:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="membership",
            name="end_date",
            field=models.DateField(),
        ),
    ]
