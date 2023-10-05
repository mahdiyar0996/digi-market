from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import (RegisterView,
                    RegisterCompleteView,
                    LoginView,
                    Logout,
                    PasswordResetTokenView,
                    PasswordResetCompleteView,
                    ProfileView,
                    ProfileChangeView,
                    ProfileBasket)
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', RegisterCompleteView.as_view(), name='email-activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('users/account-recovery/', PasswordResetTokenView.as_view(), name='account-recovery'),
    path('users/password-reset/<str:uidb64>/<str:token>/', PasswordResetCompleteView.as_view(), name='password-reset'),
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
    path('profile/personal-info/', ProfileChangeView.as_view(), name='personal_info'),
    path('profile/checkout/', ProfileBasket.as_view(), name='checkout'),
]