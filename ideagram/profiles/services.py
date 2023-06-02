from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from psycopg2 import IntegrityError
from django.core.cache import cache
from random import choice
from string import ascii_uppercase, digits

from .models import Profile, Following, ProfileLinks
from .selectors import get_user_profile, get_profile_using_username
from ..common.models import Address
from ..common.utils import update_model_instance
from ..emails.tasks import send_email_confirmation, send_email_password_confirmation
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
        data.pop('address')

    elif new_address and profile.address is None:
        address = Address.objects.create(**new_address)
        profile.address = address
        profile.save()
        data.pop('address')

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
        link=ProfileLinks(profile=profile,**data)
        link.full_clean()
        link.save()
    except IntegrityError:
        return None

    return link



@transaction.atomic
def change_password(*, username: str, validation_code: str, new_password: str) -> bool:
    profile = get_profile_using_username(username=username)
    if not profile:
        raise ValueError('Invalid username')

    cached_validation_code = cache.get(f"change_password__{username}")

    if cached_validation_code is None:
        return False

    if cached_validation_code[1] >= 3:
        return False

    if cached_validation_code[0] != validation_code.lower():
        cache.set(
            f"change_password__{username}",
            [cached_validation_code[0], cached_validation_code[1]+1],
            cache.ttl(f"change_password__{username}")
        )

    user = profile.user
    user.set_password(new_password)
    user.save()

    cache.delete(f"change_password__{username}")

    return True



def send_password_change_verification_code(*, username):
    profile = get_profile_using_username(username=username)
    if not profile:
        raise ValueError('Invalid username')

    validation_code = ''.join(choice(ascii_uppercase+digits) for i in range(6))
    user = profile.user

    cache.set(f"change_password__{username}", [validation_code.lower(), 0], 3*60)

    send_email_password_confirmation.delay(user_id=user.id, username=profile.username, validation_code=validation_code)
