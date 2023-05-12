from django.db import models
from django.db.models.query import F, Q
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Address(models.Model):
    country = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=1000, blank=True, null=True)
    zip_code = models.CharField(max_length=100, blank=True, null=True)
