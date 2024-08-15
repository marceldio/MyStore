# Generated by Django 5.0.6 on 2024-08-04 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0009_rename_photo_product_image_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="image",
        ),
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="Загрузите изображение товара",
                null=True,
                upload_to="catalog/image",
                verbose_name="Изображение",
            ),
        ),
    ]