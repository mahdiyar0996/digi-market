# Generated by Django 4.2 on 2023-10-12 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_alter_product_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductTags',
        ),
    ]
