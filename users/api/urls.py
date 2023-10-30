
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ApiUserListView, ApiUserDetailsView

urlpatterns = [
    path('users/', ApiUserListView.as_view(), name='user-list-api'),
    path('users/<int:pk>/', ApiUserDetailsView.as_view(), name='user-detail-api'),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)