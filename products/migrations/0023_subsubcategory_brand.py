# Generated by Django 4.2 on 2023-10-12 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_delete_producttags'),
    ]

    operations = [
        migrations.AddField(
            model_name='subsubcategory',
            name='brand',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]
