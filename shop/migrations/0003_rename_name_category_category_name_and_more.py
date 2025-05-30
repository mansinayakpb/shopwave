# Generated by Django 4.2.15 on 2024-08-20 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0002_alter_user_managers_product_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="category",
            old_name="name",
            new_name="category_name",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="name",
            new_name="product_name",
        ),
        migrations.AddField(
            model_name="category",
            name="cat_image",
            field=models.ImageField(blank=True, null=True, upload_to="static/"),
        ),
        migrations.AddField(
            model_name="profile",
            name="profile_picture",
            field=models.ImageField(blank=True, upload_to="profile_pictures/"),
        ),
    ]
