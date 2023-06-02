from datetime import datetime

from django.conf import settings
from config.celery import app
from hashids import Hashids
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.cache import cache

from ideagram.emails.models import Email, SentEmail
from ideagram.users.models import BaseUser


@app.task(name='verify_email', queue='email')
def send_email_confirmation(user_email, user_id, username):
    email_verify_token = cache.get(f"email_verification__{user_email}")
    if email_verify_token:
        token = email_verify_token
    else:
        hashids_verify_email = Hashids(salt=settings.EMAIL_VERIFY_SALT, min_length=10)
        token = hashids_verify_email.encode(user_id, timezone.now().microsecond)
        cache.set(
            f"email_verification__{user_email}",
            token,
            settings.EMAIL_VERIFY_EXPIRE_MINUTES * 60
        )
        cache.set(
            f"email_verification_token__{token}",
            user_email,
            settings.EMAIL_VERIFY_EXPIRE_MINUTES * 60
        )

    email_subject = "Activate your account"
    email_detail = {
        'first_name': username,
        'url': settings.EMAIL_VERIFY_URL + token
    }
    email_content = render_to_string("email/authentication/email_confirmation.html", context=email_detail)
    email = Email.objects.create(email_type='email_verification', subject=email_subject, content=email_content)
    send_mail = SentEmail.objects.create(email=email, user=BaseUser.objects.get(id=user_id))
    send_mail.send_email(sender_email=settings.EMAIL_HOST_USER)



@app.task(name='verify_email', queue='email')
def send_email_confirmation(user_id, username, validation_code):

    email_subject = "Change Password"
    email_detail = {
        'first_name': username,
        'validation_code': validation_code
    }
    email_content = render_to_string("email/authentication/change_password.html", context=email_detail)
    email = Email.objects.create(email_type='password_reset', subject=email_subject, content=email_content)
    send_mail = SentEmail.objects.create(email=email, user=BaseUser.objects.get(id=user_id))
    send_mail.send_email(sender_email=settings.EMAIL_HOST_USER)

