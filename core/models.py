from django.db import models
from main.settings import cache


class Header(models.Model):
    name = models.CharField(max_length=55, null=True)
    image = models.ImageField(upload_to='headers/')

    class Meta:
        db_table = 'headers'
        verbose_name = 'header'
        verbose_name_plural = 'headers'

    def __str__(self):
        return self.name

    @classmethod
    def filter_with_absolute_urls(cls, request, name):
        header = list(cls.objects.values_list('image').filter(name=name))
        pipeline = cache.pipeline()
        for item in range(len(header)):
            header[item] = request.build_absolute_uri("/media/" + ''.join(header[item]))
            pipeline.lpush(f'header_{name}', header[item])
        pipeline.ltrim(f'header_{name}', 0, len(header))
        pipeline.expire(f'header{name}', 3 * 60)
        pipeline.execute()
        return header
