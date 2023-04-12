from django.db import models

from ideagram.profiles.models import Profile


# Create your models here.


class ProfileReport(models.Model):
    REASON_TYPES = ["Spam", "Promoting Violence", "Encouragement to commit suicide"]

    __REASON_CHOICES = [(i.lower(), i) for i in REASON_TYPES]
    date = models.DateTimeField(auto_now_add=True)
    profile_id = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="reported_profile")
    reporter_id = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="reporter_profile")
    report_reasons = models.CharField(choices=__REASON_CHOICES, max_length=100)
    description = models.TextField(max_length=1000, blank=True, null=True)
    is_checked = models.BooleanField(default=False)
