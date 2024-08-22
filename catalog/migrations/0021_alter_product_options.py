# Generated by Django 4.2 on 2024-08-22 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0020_alter_product_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={
                "ordering": ["product", "description", "category", "price"],
                "permissions": [
                    ("can_edit_category", "Can edit category"),
                    ("can_edit_description", "Can edit description"),
                    ("can_edit_is_published", "Can edit is_published"),
                ],
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
            },
        ),
    ]
