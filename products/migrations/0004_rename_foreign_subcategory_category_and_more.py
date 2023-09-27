# Generated by Django 4.2 on 2023-09-27 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_category_avatar_subcategory_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategory',
            old_name='foreign',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='category',
            name='avatar',
            field=models.ImageField(upload_to='products/category/avatar/', verbose_name='آواتار'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='avatar',
            field=models.ImageField(upload_to='products/subcategory/avatar/', verbose_name='آواتار'),
        ),
    ]