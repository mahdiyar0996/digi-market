
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ApiUserView, ApiUserDetailsView

urlpatterns = [
    path('users/', ApiUserView.as_view(), name='user-api'),
    path('users/<int:pk>/', ApiUserDetailsView.as_view(), name='user-details-api'),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)