import uuid
from django.contrib.auth import get_user_model
from django.db import models

from ideagram.common.models import BaseModel, Address
from ideagram.common.utils import profile_upload_image_path
from ideagram.profiles.validators import special_char_not_exist_validator

BASE_USER = get_user_model()


class Profile(BaseModel, models.Model):

    GENDER_TYPES = ['male', 'female', 'other']

    __GENDER_CHOICES = [(i, i) for i in GENDER_TYPES]


    user = models.OneToOneField(BASE_USER, on_delete=models.CASCADE)
    username = models.CharField(max_length=128, unique=True, validators=[
        special_char_not_exist_validator
    ])
    first_name = models.CharField(max_length=128, null=True, blank=True)
    last_name = models.CharField(max_length=128, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=15, choices=__GENDER_CHOICES, default='other')

    bio = models.CharField(max_length=512, null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)
    profile_image = models.ImageField(upload_to=profile_upload_image_path, null=True, blank=True)

    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    idea_count = models.PositiveIntegerField(default=0)

    is_public = models.BooleanField(default=True)  # Public or Private profile
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)  # Banned by system?

    @property
    def is_visible(self):
        return self.is_public and self.is_active and not self.is_banned


    @property
    def is_profile_active(self):
        return self.is_active and not self.is_banned

    @property
    def is_profile_complete(self):
        return bool(self.first_name) and bool(self.last_name) and bool(self.address.state) and \
            bool(self.address.city) and bool(self.birth_date) and \
            ProfileLinks.objects.filter(profile=self).count() > 3

    def __str__(self):
        return f"{self.user} >> {self.username}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ProfileLinks(models.Model):

    LINK_TYPES = ['github', 'gitlab', 'telegram', 'linkedin', 'instagram', 'facebook', 'twitter']
    __LINK_TYPE_CHOICES = [(i, i) for i in LINK_TYPES]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.CharField(max_length=15, choices=__LINK_TYPE_CHOICES)
    link = models.URLField(max_length=500)
    priority = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('profile', 'type')


class Following(models.Model):
    date = models.DateField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_profile')
    profile_following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
