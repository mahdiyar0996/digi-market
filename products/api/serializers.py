from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rest_framework import serializers
from products.models import Product, ProductImage, ProductComment


class ProductImageSerializer(ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ['images']


class ProductCommentSeraializer(ModelSerializer):

    class Meta:
        model = ProductComment
        fields = ('__all__')


class ProductListSerializer(HyperlinkedModelSerializer):
    category = serializers.StringRelatedField(source='category.name', read_only=True)
    product_images = ProductImageSerializer(read_only=True, many=True, source='productimage')
    product_comments = ProductCommentSeraializer(read_only=True, many=True, source='productcomment')

    class Meta:
        model = Product
        fields = ['id', 'url', 'category', 'name', 'brand', 'description', 'details',
                  'warranty', 'price', 'discount', 'is_active', 'colour',
                  'stock', 'avatar', 'created_at', 'updated_at', 'product_images' ,'product_comments']
        extra_kwargs = {
            'url': {'view_name': 'product-details-api'}
        }


class ProductDetailsSerializer(ModelSerializer):
    sub_sub_category = serializers.StringRelatedField(source='category.name', read_only=True)
    sub_category = serializers.StringRelatedField(source='category.category.name', read_only=True)
    category = serializers.StringRelatedField(source='category.category.category.name', read_only=True)
    product_images = ProductImageSerializer(read_only=True, many=True, source='productimage')
    product_comments = ProductCommentSeraializer(read_only=True, many=True, source='productcomment')

    class Meta:
        model = Product
        fields = ['id', 'category', 'sub_category', 'sub_sub_category', 'name', 'brand', 'description', 'details',
                  'warranty', 'price', 'discount', 'is_active', 'colour',
                  'stock', 'avatar', 'product_images', 'product_comments']