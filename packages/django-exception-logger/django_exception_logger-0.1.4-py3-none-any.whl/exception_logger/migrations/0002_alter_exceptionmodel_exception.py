# Generated by Django 4.2.8 on 2024-04-16 08:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exception_logger", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exceptionmodel",
            name="exception",
            field=models.TextField(),
        ),
    ]
