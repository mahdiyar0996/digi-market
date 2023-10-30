from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ApiProductListView, ApiProductDetailsView

urlpatterns = [
    path('products/', ApiProductListView.as_view(), name='product-list-api'),
    path('products/<int:pk>/', ApiProductDetailsView.as_view(), name='product-details-api'),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)