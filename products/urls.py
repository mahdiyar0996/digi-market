from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import CategoryListView, ProductListView, ProductDetailsView

urlpatterns = [
    path('category/<str:category>/', CategoryListView.as_view(), name='subcategory'),
    path('category/<str:category>/products/', ProductListView.as_view(), name='product-list'),
    path('category/<str:category>/<int:product_id>/', ProductDetailsView.as_view(), name='product-details'),
]