from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib import messages
from smtplib import SMTPException
from django.contrib.auth.tokens import PasswordResetTokenGenerator as Prtg


def send_token_email(request, user, email:dict):
    mail_subject = email.get('subject')
    to_email = email.get('to_email')
    message = render_to_string(email.get('template'), {
        'user': email.get('user'),
        'domain': email.get('domain'),
        'uid': email.get('uid'),
        'token': email.get('token'),
    })
    headers = {'Importance': 'important'}
    send_email = EmailMessage(mail_subject, message, to=[to_email], headers=headers)
    try:
        send_email.send()
        messages.success(request, email.get('success_msg'), 'success')
    except SMTPException:
        messages.error(request, {email.get('error_msg')}, 'danger')
