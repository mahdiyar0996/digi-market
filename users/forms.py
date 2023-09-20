import re
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm as BaseForm
from .models import User
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
    password1 = forms.CharField(required=True,validators=[valid_password()],
                               widget=forms.PasswordInput,
                                help_text="رمز عبور باید ۸ کاراکتر یا بیشتر باشد")
    password2 = forms.CharField(required=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(("رمز عبور تکرار شده مطابقت ندارد."))
        return password1



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
                               error_messages={'unique': 'این نام کاربری قبلا انتخاب شده است'})
    password = forms.CharField(max_length=55, required=True, validators=[valid_password()],
                               error_messages={'invalid': 'رمز عبور باید حداقل ۸ کاراکتر و یک حرف بزرگ داشته باشد'})
    remember = forms.BooleanField(widget=forms.CheckboxInput)


    def clean_username(self):
        username = self.cleaned_data.get('username')

        if '@' in username:
            validate = search('/^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$/', username)
            if not validate:
                raise ValidationError("لطفا یک ایمیل معتبر وارد کنید")
        else:
            validate = search('([a-zA-Z0-9_]+)', username)
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

