# Generated by Django 4.2 on 2023-09-25 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='headers/')),
            ],
            options={
                'verbose_name': 'header',
                'verbose_name_plural': 'headers',
                'db_table': 'headers',
            },
        ),
    ]