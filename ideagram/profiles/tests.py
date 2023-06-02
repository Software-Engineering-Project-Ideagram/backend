from django.core.exceptions import ValidationError
from django.test import TestCase

from ideagram.profiles.models import Profile, Following
from ideagram.profiles.services import follow_profile,register,update_user_profile
from ideagram.users.Exceptions import InvalidPassword
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

    def test_following_a_user(self):
        profile1 = Profile.objects.get(username="user1")
        profile2 = Profile.objects.get(username="user2")
        user1 = profile1.user

        follow_profile(user=user1, following_username=profile2.username)

        temp = Following.objects.filter(profile=profile1, profile_following=profile2)
        self.assertEqual(len(temp), 1)

        profile1 = Profile.objects.get(username="user1")
        profile2 = Profile.objects.get(username="user2")
        self.assertEqual(profile1.following_count, 1)
        self.assertEqual(profile2.follower_count, 1)

        self.assertEqual(profile1.follower_count, 0)
        self.assertEqual(profile2.following_count, 0)

    def test_following_a_followed_profile(self):
        profile1 = Profile.objects.get(username="user1")
        profile2 = Profile.objects.get(username="user2")
        user1 = profile1.user

        follow_profile(user=user1, following_username=profile2.username)

        with self.assertRaises(ValueError):
            follow_profile(user=user1, following_username=profile2.username)

        profile1 = Profile.objects.get(username="user1")
        profile2 = Profile.objects.get(username="user2")

        self.assertEqual(profile1.following_count, 1)
        self.assertEqual(profile2.follower_count, 1)

        self.assertEqual(profile1.follower_count, 0)
        self.assertEqual(profile2.following_count, 0)


class UserTest(TestCase):
    def test_create_user_in_registeration(self):
       user1= register(username="user1",email="user1@gmail.com",password="user1password")
       self.assertEqual(str(type(user1)),"<class 'ideagram.users.models.BaseUser'>")
       with self.assertRaises(ValueError):
           user2 = register(username="user2", email="", password="user1password")

       with self.assertRaises(ValidationError):
           user2 = register(username="user1", email="user2@gmail.com", password="user1password")


class UpdateProfileTest(TestCase):

    def setUp(self):
        baseuser1 = BaseUser.objects.create_user(email="user1@gmail.com",
                                                 password="userpass",
                                                 is_active=True, is_admin=False)

        baseuser1.is_email_verified = True
        baseuser1.save()
        profile1 = Profile.objects.create(user=baseuser1, username="user1")
    def test_invalid_user_authenticate(self):
        data={"new_password":"newpass",
              "old_password":"pldpass"}
        with self.assertRaises(InvalidPassword):
            user= update_user_profile(profile=Profile.objects.get(username="user1"),data=data)


    def test_valid_user_authenticate(self):
        data={"new_password":"newpass",
              "old_password":"userpass"}

        user= update_user_profile(profile=Profile.objects.get(username="user1"),data=data)
        self.assertEqual(str(type(user)),"<class 'ideagram.profiles.models.Profile'>")