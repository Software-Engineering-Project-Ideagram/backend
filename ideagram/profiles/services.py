from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Profile

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