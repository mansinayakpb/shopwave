# Generated by Django 4.2.15 on 2024-08-26 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0003_rename_name_category_category_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="username",
        ),
    ]
