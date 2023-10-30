from rest_framework import generics
from products.models import Product
from .serializers import ProductListSerializer, ProductDetailsSerializer
from utils.decorators import debugger
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ApiProductListView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('productimage', 'productcomment').select_related('category').all()
    serializer_class = ProductListSerializer

    @debugger
    @method_decorator(cache_page(60 * 2, key_prefix='products-list'))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ApiProductDetailsView(generics.RetrieveAPIView,
                            generics.UpdateAPIView):
    serializer_class = ProductDetailsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @method_decorator(cache_page(60 * 10, key_prefix='products-details'))
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_queryset(self):
        try:
            query = Product.objects.select_related('category', 'category__category',
                                                   'category__category__category'
                                                   ).prefetch_related('productimage', 'productcomment'
                                                                      ).defer('created_at', 'updated_at',
                                                                              'category__created_at',
                                                                              'category__updated_at',
                                                                              'category__details',
                                                                              'category__brand',
                                                                              'category__avatar',
                                                                              'category__category__created_at',
                                                                              'category__category__updated_at',
                                                                              'category__category__avatar',
                                                                              'category__category__category__updated_at',
                                                                              'category__category__category__avatar',
                                                                              'category__category__category__created_at',
                                                                              ).get(pk=self.kwargs.get('pk'))
        except Product.DoesNotExist:
            query = None
        return query

    def get_object(self):
        queryset = self.get_queryset()
        self.check_object_permissions(self.request, queryset)
        return queryset
