from django.shortcuts import render, redirect
from django.views import View
from django.views import generic
from django.contrib.auth import login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from .forms import RegisterForm, LoginForm, PasswordResetSendTokenForm, PasswordResetForm, UserForm, ProfileForm
from .tokens import email_verification_token
from .models import User
from .backends import EmailUsernameAuthentication as Eua
from django.contrib.auth.tokens import PasswordResetTokenGenerator as Prtg
from utils.email_senders import send_token_email
from utils.decorators import debugger
from datetime import datetime
from django.contrib.auth.decorators import login_required




class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            send_token_email(request, user, {'subject': "دیجی مارکت",
                                             'to_email': form.cleaned_data.get('email'),
                                             'template': 'email/user_activision_email.html',
                                             'user': user,
                                             'domain': current_site.domain,
                                             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                             'token': email_verification_token.make_token(user),
                                             'success_msg': 'ایمیل تایید به ایمیل شما ارسال شد',
                                             'error_msg': 'کل در ارسال ایمیل تایید دوباره امتحان کنید'
                                             })
            return render(request, 'register.html', {'form': form})
        context = {'form': form}
        return render(request, 'register.html', context)


class UserActivationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            messages.error('request', 'لینک تایید اشتباه است')
            return redirect('login')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data['remember']
            email = None
            if '@' in username:
                email = username
                username = None
            user = Eua.authenticate(request, username=username,
                                    email=email, password=password)
            user.ipaddress = request.META.get('REMOTE_ADDR')
            user.save()
            if user is not None:
                if remember:
                    request.session.set_expiry(0)
                login(request, user)
                return redirect('register')
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است', 'danger')
        return render(request, 'login.html', {'form': form})

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
        user = request.user
        profile = user.profile
        return render(request, 'profile.html', {'user': user, 'profile': profile})


class ProfileChangeView(View):
    def get(self, request):
        user = request.user
        profile = user.profile
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm
        return render(request, 'personal_info.html', {'user_form': user_form,
                                                      'profile_form': profile_form,
                                                      'user': user,
                                                      'profile': profile})
    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        user_form.password = request.user.password
        if user_form.is_valid() and profile_form.is_valid():
            print('sdssad')
            if user_form.password:
                user_form.set_password(user_form.password)
            user_form.save()
            profile_form.save()
            return redirect('profile')
        print(user_form.errors, profile_form.errors)
        return render(request, 'personal_info.html', {'user_form': user_form, "profile_form": profile_form,
                                                      'user': request.user, 'profile': request.user.profile})







