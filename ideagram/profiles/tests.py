from django.core.exceptions import ValidationError
from django.test import TestCase

from ideagram.common.models import Address
from ideagram.profiles.models import Profile, Following
from ideagram.profiles.selectors import get_profile_using_username
from ideagram.profiles.services import follow_profile, register, update_user_profile, add_social_media_to_profile
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

    def test_change_profile_address(self):
        old_address = {"country": "country1", "state": "state1", "city": "city1", "address": "address1",
                       "zip_code": "zip_code1"}

        data = {"address": old_address}

        old_profile = Profile.objects.get(username="user1")
        new_profile = update_user_profile(profile=old_profile, data=data)

        self.assertEquals(new_profile.address.country, old_address["country"])
        self.assertEquals(new_profile.address.state, old_address["state"])
        self.assertEquals(new_profile.address.city, old_address["city"])
        self.assertEquals(new_profile.address.address, old_address["address"])
        self.assertEquals(new_profile.address.zip_code, old_address["zip_code"])

    def test_validate_link_url(self):
        data1 = {"type": "telegram", "link": "test"}
        data2 = {"type": "telegram", "link": "https://telegram.com"}
        profile = Profile.objects.get(username="user1")
        with self.assertRaises(ValidationError):
            link = add_social_media_to_profile(profile=profile, data=data1)

        link = add_social_media_to_profile(profile=profile, data=data2)
        self.assertEqual(link.link, "https://telegram.com")
        self.assertEqual(link.type, "telegram")

    def test_duplicated_link(self):
        data = {"type": "instagram", "link": "https://instagram.com"}
        profile = Profile.objects.get(username="user1")
        link = add_social_media_to_profile(profile=profile, data=data)
        with self.assertRaises(ValidationError):
            link = add_social_media_to_profile(profile=profile, data=data)


class ProfileTest(TestCase):
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

        profile1 = Profile.objects.create(user=baseuser1, username="user1", is_public=True, is_active=True,
                                          is_banned=False)
        profile2 = Profile.objects.create(user=baseuser2, username="user2", is_public=True, is_active=True,
                                          is_banned=True)

        baseuser3 = BaseUser.objects.create_user(email="user3@gmail.com",
                                                 password="user3",
                                                 is_active=True, is_admin=False)

        baseuser3.is_email_verified = True
        baseuser3.save()

        profile3 = Profile.objects.create(user=baseuser3, username="user3", is_public=True, is_active=True,
                                          is_banned=True)
        profile3.first_name = "user3firstName"
        profile3.last_name = "user3lastName"
        profile3.birth_date = "1400-11-20"
        profile3.address = Address.objects.create(city="city1",state="state1")
        profile3.save()

    def test_is_visible(self):
        baseuser1=BaseUser.objects.get(email="user1@gmail.com")
        baseuser2=BaseUser.objects.get(email="user2@gmail.com")
        profile1=Profile.objects.get(user=baseuser1, username="user1")
        profile2=Profile.objects.get(user=baseuser2, username="user2")
        self.assertTrue(profile1.is_visible)
        self.assertFalse(profile2.is_visible)
    def test_is_profile_active(self):
        baseuser1 = BaseUser.objects.get(email="user1@gmail.com")
        baseuser2 = BaseUser.objects.get(email="user2@gmail.com")
        profile1 = Profile.objects.get(user=baseuser1, username="user1")
        profile2 = Profile.objects.get(user=baseuser2, username="user2")
        self.assertTrue(profile1.is_visible)
        self.assertFalse(profile2.is_visible)

    def test_str(self):
        baseuser1 = BaseUser.objects.get(email="user1@gmail.com")
        baseuser2 = BaseUser.objects.get(email="user2@gmail.com")
        profile1 = Profile.objects.get(user=baseuser1, username="user1")
        profile2 = Profile.objects.get(user=baseuser2, username="user2")
        self.assertEqual(str(profile1),"user1@gmail.com >> user1")
        self.assertEqual(str(profile2),"user2@gmail.com >> user2")

    def test_is_profile_complete(self):
        baseuser1 = BaseUser.objects.get(email="user1@gmail.com")
        baseuser2 = BaseUser.objects.get(email="user2@gmail.com")
        profile1 = Profile.objects.get(user=baseuser1, username="user1")
        profile2 = Profile.objects.get(user=baseuser2, username="user2")
        baseuser3 = BaseUser.objects.get(email="user3@gmail.com")
        profile3 = Profile.objects.get(user=baseuser3, username="user3")
        self.assertFalse(profile1.is_profile_complete)
        self.assertFalse(profile2.is_profile_complete)
        self.assertTrue(profile3.is_profile_complete)


class SelectorTest(TestCase):
    def setUp(self):
        baseuser1 = BaseUser.objects.create_user(email="user1@gmail.com",
                                                 password="user",
                                                 is_active=True, is_admin=False)
        baseuser1.is_email_verified = True
        baseuser1.save()
        profile1 = Profile.objects.create(user=baseuser1, username="user1", is_public=True, is_active=True,
                                          is_banned=False)

    def test_get_profile_using_username(self):
        profile1=get_profile_using_username(username="user1")
        profile2=get_profile_using_username(username="user2")
        self.assertEqual(profile1.username,"user1")
        self.assertEqual(profile2,None)