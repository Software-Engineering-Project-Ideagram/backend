from django.test import TestCase

from ideagram.profiles.models import Profile, Following
from ideagram.profiles.services import follow_profile
from ideagram.users.models import BaseUser


class FollowProfileTest(TestCase):
    def setUp(self):
        baseuser1 = BaseUser.objects.create_user(email="user1@gmail.com",
                                password="user",
                                is_active=True, is_admin=False)

        baseuser2 = BaseUser.objects.create_user(email="user2@gmail.com",
                                                 password="user",
                                                 is_active=True, is_admin=False)

        baseuser1.is_email_verified = True
        baseuser2.is_email_verified = True

        baseuser1.save()
        baseuser2.save()

        profile1 = Profile.objects.create(user=baseuser1, username="user1")
        profile2 = Profile.objects.create(user=baseuser2, username="user2")

    def test_following_not_existence_profile(self):
        profile1 = Profile.objects.get(username="user1")
        user1 = profile1.user
        with self.assertRaises(Profile.DoesNotExist):
            follow_profile(user=user1, following_username='user3')

   