import re
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm as BaseForm
from .models import User, Profile
from re import search
from django.core.validators import ValidationError
from utils.validators import valid_email, valid_username, valid_password, valid_phone_number
class BaseUserCreationForm(BaseForm):
    password1 = forms.CharField(max_length=55, required=True,
                                help_text="رمز عبور باید ۸ کاراکتر یا بیشتر باشد",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=55, required=True,
                                help_text="رمز عبور خود را دوباره وارد کنید",
                                widget=forms.PasswordInput)


    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("رمز عبور مطابقت ندارد")
        return password1, password2





class RegisterForm(forms.ModelForm):
    # username = forms.CharField(required=True,validators=[valid_username()],
    #                            error_messages={'unique': 'کاربری با این نام وجود دارد!'})
    #
    # email = forms.EmailField(required=True, validators=[valid_email()],
    #                          error_messages={'unique': 'کاربری با این ایمیل وجود دارد!'})
    password1 = forms.CharField(required=True, validators=[valid_password()],
                               widget=forms.PasswordInput,
                                help_text="رمز عبور باید ۸ کاراکتر یا بیشتر باشد")
    password2 = forms.CharField(required=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def clean(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(("رمز عبور تکرار شده مطابقت ندارد."))
        return self.cleaned_data





    # def is_valid(self):

    #
    #
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if re.search('^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$',
    #                  email) is None:
    #         raise ValidationError('ایمیل وارد شده معتبر نمی باشد')
    #     if User.objects.filter(email=email).exists():
    #         raise ValidationError('کاربری با این ایمیل وجود دارد')
    #     return email
    #
    # def clean(self):
    #     try:
    #         if 'Enter' in self.errors.get('email'):
    #             self.errors['email'].pop(0)
    #     except TypeError:
    #         pass




class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True,
                               error_messages={'unique': 'این نام کاربری قبلا انتخاب شده است',})
    password = forms.CharField(max_length=55, required=True)
    remember = forms.BooleanField(widget=forms.CheckboxInput, required=False)


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            validate = search(r'^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$', username)
            if not validate:
                raise ValidationError("لطفا یک ایمیل معتبر وارد کنید")
        else:
            validate = search(r'([a-zA-Z0-9_]+)', username)
            if not validate:
                raise ValidationError("نام کاربری نباید از حروف !٬#$%^&*()باشد")
        return username


class PasswordResetSendTokenForm(forms.Form):
    email = forms.EmailField(required=True,
                             validators=[valid_email()],
                             error_messages={'invalid': 'لطفا یک ایمیل معتبر وارد کنید'})


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(max_length=55, help_text='رمز عبور جدید خود را وارد کنید',
                                required=True,
                                widget=forms.PasswordInput,
                                validators=[valid_password()])
    password2 = forms.CharField(max_length=55, help_text='رمز خود را تکرار کنید',
                                required=True,
                                widget=forms.PasswordInput, )


class UserForm(forms.Form):
    username = forms.CharField(label='نام کاربری', max_length=55, required=False)
    email = forms.EmailField(label='ایمیل', max_length=55, required=False)
    password = forms.CharField(label='رمز عبور', max_length=55, widget=forms.PasswordInput, required=False)
    phone_number = forms.CharField(label='شماره موبایل', max_length=11, required=False)
    city = forms.CharField(label='شهر', max_length=55, required=False)
    address = forms.CharField(label='ادرس', max_length=255, required=False)
    first_name = forms.CharField(label='نام', max_length=55, required=False)
    last_name = forms.CharField(label='نام خانوادگی', max_length=55, required=False)
    birthday = forms.IntegerField(label='تاریخ تولد', required=False, widget=forms.NumberInput)
    job = forms.CharField(label='شغل', max_length=55, required=False)

    # class Meta:
    #     model = User
    #     fields = ['username', 'email', 'password', 'phone_number', 'city', 'address']

        # self.ins
        # profile.first_name = cd['first_name']
        # profile.last_name = cd['last_name']
        # profile.birthday = cd['birthday']
        # profile.job = cd['job']
        # profile.save()


#
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['first_name', 'last_name', 'birthday', 'job']