from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from .models import Profile
from ..common.utils import update_model_instance
from ..users.Exceptions import InvalidPassword

BASE_USER = get_user_model()


def create_profile(*, user: BASE_USER, username: str) -> Profile:
    return Profile.objects.create(user=user, username=username)


def create_user(*, email: str, password: str) -> BASE_USER:
    return BASE_USER.objects.create_user(email=email, password=password)


@transaction.atomic
def register(*, username: str, email: str, password: str) -> BASE_USER:
    user = create_user(email=email, password=password)
    create_profile(user=user, username=username)

    return user


@transaction.atomic
def update_user_profile(*, profile: Profile, data: dict) -> Profile:
    if data.get('new_password', None):
        user = authenticate(email=profile.user.email, password=data['old_password'])
        if user:
            user.set_password(data['new_password'])
            user.save()
        else:
            raise InvalidPassword("Invalid password")

    updated_profile = update_model_instance(instance=profile, data=data)
    return updated_profile
