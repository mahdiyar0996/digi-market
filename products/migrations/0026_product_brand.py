# Generated by Django 4.2 on 2023-10-16 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_subsubcategory_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='برند'),
        ),
    ]
