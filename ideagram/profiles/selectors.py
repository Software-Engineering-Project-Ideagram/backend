from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from ideagram.profiles.models import Profile, ProfileLinks

BASE_USER = get_user_model()


def get_user_profile(*, user: BASE_USER) -> Profile:
    """returns given user's profile"""
    return Profile.objects.get(user=user)


def get_profile_social_media(*, profile: Profile) -> QuerySet(ProfileLinks):
    """Returns social media links of given profile"""

    return ProfileLinks.objects.filter(profile=profile).order_by('priority')


def get_profile_using_username(*, username: str) -> Profile | None:
    profiles = Profile.objects.filter(username=username)
    if profiles.exists():
        return profiles.first()

    return None
