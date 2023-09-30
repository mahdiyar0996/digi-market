from django.db import models


class ProductManager(models.Manager):

    def create(self, *args, **kwargs):
        model = self.model(**kwargs)
        model.productimage.images = model.avatar
        model.productimage.model = model
        model.save()
        model.productimage.save()
        return model


