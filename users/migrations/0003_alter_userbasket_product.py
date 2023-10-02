# Generated by Django 4.2 on 2023-10-02 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_alter_productcomment_comment'),
        ('users', '0002_alter_profile_table_userbasket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbasket',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='products.product', unique=True, verbose_name='کالا'),
        ),
    ]
