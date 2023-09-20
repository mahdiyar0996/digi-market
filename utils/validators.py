from django.core.validators import ValidationError, RegexValidator, MinLengthValidator


def valid_email():
    validator = RegexValidator('^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$',
                   message='ایمیل وارد شده معتبر نمی باشد',
                   code='invalid')
    return validator


def valid_username():
    validator = RegexValidator('([a-zA-Z0-9_]+)',
                   message='نام کاربری نباید از حروف !٬#$%^&*()باشد', code='invalid')
    return validator


def valid_phone_number():
    validator = RegexValidator('(^09)([0-9]{9)', code='invalid',
                   message='شماره وارد شده معتبر نمی باشد',)
    return validator


def valid_password():
    validator = RegexValidator('^([\b\w\d]*)([A-Z]+)([\b\w\d]*)', code='invalid',
                   message='رمز عبور حداقل باید ۸ کاراکتر یا بیشتر باشد و حداقل یک حرف بزرگ داشته باشد')
    return validator





