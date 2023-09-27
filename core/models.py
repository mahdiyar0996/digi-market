from django.db import models

class Header(models.Model):
    name = models.CharField(max_length=55, null=True)
    image = models.ImageField(upload_to='headers/')

    class Meta:
        db_table = 'headers'
        verbose_name = 'header'
        verbose_name_plural = 'headers'

    def __str__(self):
        return self.name