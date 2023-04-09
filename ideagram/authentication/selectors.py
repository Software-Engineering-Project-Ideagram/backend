from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from ideagram.profiles.models import Profile

BASE_USER = get_user_model()


def get_user_from_username(*, username: str) -> BASE_USER | None:

    profile = Profile.objects.filter(
        username=username, is_banned=False, is_active=True
    ).select_related('user')

    if profile.exists():
        return profile.first().user

    return None
    