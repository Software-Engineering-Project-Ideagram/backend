from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from ideagram.profiles.models import Profile, ProfileLinks, Following

BASE_USER = get_user_model()


def get_user_profile(*, user: BASE_USER) -> Profile:
    """returns given user's profile"""
    return Profile.objects.get(user=user)



def get_general_user_profile(*, username: str) -> Profile | None:
    """returns given user's profile"""
    try:
        return Profile.objects.get(username=username, is_active=True, is_banned=False, is_public=True)
    except Profile.DoesNotExist:
        return None


def get_profile_social_media(*, profile: Profile) -> QuerySet(ProfileLinks):
    """Returns social media links of given profile"""

    return ProfileLinks.objects.filter(profile=profile)


def get_profile_using_username(*, username: str) -> Profile | None:
    profiles = Profile.objects.filter(username=username)
    if profiles.exists():
        return profiles.first()

    return None


def get_profile_followers(*, profile: Profile) -> list:
    followers = Following.objects.filter(profile_following=profile)
    return [x.profile for x in followers]


def get_profile_followings(*, profile: Profile) -> list:
    followers = Following.objects.filter(profile=profile)
    return [x.profile_following for x in followers]
