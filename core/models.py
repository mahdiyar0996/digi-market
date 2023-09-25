from django.db import models

class Header(models.Model):
    image = models.ImageField(upload_to='headers/')

    class Meta:
        db_table = 'headers'
        verbose_name = 'header'
        verbose_name_plural = 'headers'
