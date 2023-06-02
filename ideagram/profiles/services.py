from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from psycopg2 import IntegrityError

from .models import Profile, Following, ProfileLinks
from .selectors import get_user_profile
from ..common.models import Address
from ..common.utils import update_model_instance
from ..emails.tasks import send_email_confirmation
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
    send_email_confirmation.delay(user_id=user.id, user_email=email, username=username)
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

    new_address = data.get('address', None)

    if new_address and profile.address is not None:
        updated_address = update_model_instance(instance=profile.address, data=new_address)

    elif new_address and profile.address is None:
        address = Address.objects.create(**new_address)
        profile.address = address
        profile.save()

    updated_profile = update_model_instance(instance=profile, data=data)
    return updated_profile


@transaction.atomic
def follow_profile(*, user, following_username):
    following = Profile.objects.get(username=following_username)
    follower = get_user_profile(user=user)

    temp = Following.objects.filter(profile=follower, profile_following=following)

    if temp.exists():
        raise ValueError("These profiles already followed each other")

    Following.objects.create(profile=follower, profile_following=following)

    follower.following_count += 1
    following.follower_count += 1
    follower.save()
    following.save()


@transaction.atomic
def add_social_media_to_profile(*, profile: Profile, data) -> ProfileLinks | None:
    try:
        link = ProfileLinks.objects.create(profile=profile, **data)
    except IntegrityError:
        return None

    return link
