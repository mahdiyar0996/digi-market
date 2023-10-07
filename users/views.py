from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from .forms import RegisterForm, LoginForm, PasswordResetSendTokenForm, PasswordResetForm, UserForm
from .tokens import email_verification_token
from .models import User, Profile, UserBasket
from .backends import EmailUsernameAuthentication as Eua
from django.contrib.auth.tokens import PasswordResetTokenGenerator as Prtg
from utils.email_senders import send_token_email
from utils.decorators import debugger
from datetime import datetime
from main.settings import cache
import json
from django.core.cache import cache as django_cache


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'register.html', context)

    def post(self, request):
        initial_dict = {
            "username": request.POST.get('username'),
            "email": request.POST.get('email'),
        }
        form = RegisterForm(request.POST, initial=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'],
                                            email=cd['email'], password=cd['password1'],
                                            is_active=False)
            current_site = get_current_site(request)
            send_token_email(request, user, {'subject': "دیجی مارکت",
                                             'to_email': form.cleaned_data.get('email'),
                                             'template': 'email/user_activision_email.html',
                                             'user': user,
                                             'domain': current_site.domain,
                                             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                             'token': email_verification_token.make_token(user),
                                             'success_msg': 'ایمیل تایید به ایمیل شما ارسال شد',
                                             'error_msg': 'مشکل در ارسال ایمیل تایید دوباره امتحان کنید'
                                             })
            return render(request, 'register.html', {'form': form})
        context = {'form': form}
        return render(request, 'register.html', context, status=400)


class RegisterCompleteView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user and email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            messages.error('request', 'لینک تایید اشتباه است')
            return redirect('login')


class LoginView(View):
    @debugger
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    @debugger
    def post(self, request):
        form = LoginForm(request.POST, initial=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            if '@' in username:
                user = Eua.authenticate(request, email=username, password=password)
            else:
                user = Eua.authenticate(request, username=username, password=password)
            if user is not None:
                user.ipaddress = request.META.get('REMOTE_ADDR')
                user.save()
                request.session['sessionid'] = user.id
                if remember is True:
                    request.session.set_expiry(0)
                request.session.set_expiry(60 * 60 * 24)
                login(request, user)
                return redirect('profile')
            return render(request, 'login.html', {'form': form}, status=400)
        messages.error(request, 'نام کاربری یا رمز عبور اشتباه است', 'danger')
        return render(request, 'login.html', {'form': form}, status=400)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class PasswordResetTokenView(View):
    def get(self, request):
        form = PasswordResetSendTokenForm()
        return render(request, 'password_reset_send_token.html', {"form": form})

    def post(self, request):
        form = PasswordResetSendTokenForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email__exact=email)
                current_site = get_current_site(request)
                send_token_email(request, user, {'subject': "بازیابی رمز عبور",
                                                 'to_email': form.cleaned_data.get('email'),
                                                 'template': 'email/user_password_reset_message.html',
                                                 'user': user,
                                                 'domain': current_site.domain,
                                                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                                 'token': Prtg().make_token(user),
                                                 'success_msg': 'ایمیل بازیابی به ایمیل شما ارسال شد',
                                                 'error_msg': 'مشکل در ارسال ایمیل باز یابی دوباره امتحان کنید'
                                                 })
            except User.DoesNotExist:
                messages.error(request, "کاربری با این ایمیل وجود ندارد", 'danger')
        return render(request, 'password_reset_send_token.html', {'form': form})


class PasswordResetCompleteView(View):
    def get(self, request, uidb64, token):
        form = PasswordResetForm()
        return render(request, 'password-reset-complete.html', {'form': form})

    def post(self, request, uidb64, token):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 != password2:
                messages.error(request, 'رمز عبور با تکرار رمز مطابقت ندارد', 'danger')
                return render(request, 'password-reset-complete.html', {'form': form})
            try:
                user = User.objects.get(pk=urlsafe_base64_decode(uidb64))
            except User.DoesNotExist:
                user = None
            if user and Prtg().check_token(user, token):
                user.set_password(password1)
                user.last_password_reset = datetime.now()
                user.save()
                messages.success(request, 'رمز عبور شما با موفقیت تغییر پیدا کرد ', 'success')
                return redirect('login')
            messages.error(request, 'لینک باز یابی معتبر نمی باشد', 'danger')
        return render(request, 'password-reset-complete.html', {'form': form})


class ProfileView(View):
    @debugger
    def get(self, request):
        user = cache.hgetall(f'user{request.session["sessionid"]}')
        profile = cache.hgetall(f'profile{request.session["sessionid"]}')
        if not any([len(user) > 0, len(profile) > 0]):
            user, profile = Profile().get_user_and_profile(request, request.user)
        return render(request, 'profile.html', {'user': user, 'profile': profile})


class ProfileChangeView(View):
    @debugger
    def get(self, request):
        user = cache.hgetall(f'user{request.session["sessionid"]}')
        profile = cache.hgetall(f'profile{request.session["sessionid"]}')
        if not any([len(user) > 0, len(profile) > 0]):
            user, profile = Profile.get_user_and_profile(request, request.user)
        data = user | profile
        form = UserForm(initial=data)
        return render(request, 'personal_info.html', {'form': form,
                                                      'profile': profile,
                                                      'user': user})
    def post(self, request):
        user = request.user
        form = UserForm(request.POST, initial=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user.save(**cd)
            user.profile.save(**cd)
            return redirect('profile')
        return render(request, 'personal_info.html', {'form': form, 'user': user,
                                                      'profile': user.profile})


class ProfileBasketView(View):
    @debugger
    def get(self, request):
        user = cache.hgetall(f"user{request.session.get('sessionid', False)}")
        profile = cache.hgetall(f"profile{request.session.get('sessionid', False)}")
        products = django_cache.get(f"user_basket{request.session.get('sessionid', False)}")
        if user and products:
            user, profile = Profile.get_user_and_profile(request, request.user)
        if products:
            products = products = UserBasket.filter_basket_products(request, request.user)
        return render(request, 'profile-basket.html', {'products': products, 'user': user, 'profile': profile})




