from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import CategoryListView, SubCategoryListView, ProductDetailsView, SubSubCategoryList

urlpatterns = [
    path('', include('products.api.urls')),
    path('category/<str:category>/', CategoryListView.as_view(), name='category-list'),
    path('subcategory/<str:category>/', SubCategoryListView.as_view(), name='subcategory-list'),
    path('category/<str:category>/products/', SubSubCategoryList.as_view(), name='sub-subcategory-list'),
    path('category/<str:category>/<int:product_id>/', ProductDetailsView.as_view(), name='product-details'),
]