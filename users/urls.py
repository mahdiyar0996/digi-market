from django.contrib import admin
from django.urls import path, include
from .views import (RegisterView,
                    UserActivationView,
                    LoginView,
                    PasswordResetTokenView,
                    PasswordResetCompleteView)
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', UserActivationView.as_view(), name='email-activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/account-recovery/', PasswordResetTokenView.as_view(), name='account-recovery'),
    path('users/password-reset/<str:uidb64>/<str:token>/', PasswordResetCompleteView.as_view(), name='password-reset')
]