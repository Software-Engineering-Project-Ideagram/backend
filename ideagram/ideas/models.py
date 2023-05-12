import uuid as uuid
from django.db import models

from ideagram.common.models import BaseModel
from ideagram.common.utils import idea_upload_image_path
from ideagram.profiles.models import Profile


# Create your models here.


class Classification(models.Model):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=50, unique=True)


class Idea(BaseModel):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    classification = models.ManyToManyField(Classification)
    title = models.CharField(max_length=100)
    goal = models.CharField(max_length=500)
    abstract = models.CharField(max_length=1500)
    description = models.TextField()
    image = models.ImageField(upload_to=idea_upload_image_path, null=True, blank=True)

    attached_files_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    max_donation = models.PositiveIntegerField(default=0)  # required donation
    total_donation = models.PositiveIntegerField(default=0)  # total donation amount

    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)
    show_likes = models.BooleanField(default=True)
    show_views = models.BooleanField(default=True)
    show_comments = models.BooleanField(default=True)


class EvolutionStep(models.Model):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    finish_date = models.DateField()
    description = models.CharField(max_length=200)
    priority = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('idea', 'priority')


class FinancialStep(models.Model):
    FINANCIAL_UNIT_TYPES = ['rial', 'dollar', 'euro']
    __FINANCIAL_UNIT_CHOICES = [(x, x.lower()) for x in FINANCIAL_UNIT_TYPES]

    uuid = models.UUIDField(editable=False, default=uuid.uuid4)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    cost = models.PositiveIntegerField()
    description = models.CharField(max_length=200)
    unit = models.CharField(max_length=20, choices=__FINANCIAL_UNIT_CHOICES)
    priority = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('idea', 'priority')


class IdeaComment(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    idea = models.ForeignKey(to=Idea, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)


class Organization(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=200)
