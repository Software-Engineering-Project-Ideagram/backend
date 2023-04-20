from django.db import models
from ideagram.users.models import BaseUser


class Email(models.Model):
    EMAIL_TYPE_CHOICES = (
        ("email_verification", "email_verification"),
        ("password_reset", "password_reset"),
        ("notification", "notification"),
    )
    email_type = models.CharField(choices=EMAIL_TYPE_CHOICES, max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=150)
    content = models.TextField()


class SentEmail(models.Model):
    email_id = models.ForeignKey(Email, on_delete=models.CASCADE)
    user_id = models.ForeignKey(BaseUser, on_delete=models.CASCADE)

