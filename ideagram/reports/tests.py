from django.test import TestCase

from ideagram.profiles.models import Profile
from ideagram.reports.services import create_profile_report
from ideagram.users.models import BaseUser


class ReportsTest(TestCase):

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

    def test_does_not_exist_reported_profile(self):
        data={
            "profile_username":"user3",
            "report_reasons": "Spam",
            "description": "Spam",
        }
        reporter_profile=Profile.objects.get(username="user1")
        with self.assertRaises(ValueError):
            profile_report=create_profile_report(reporter=reporter_profile, data=data)

    def test_exist_reported_profile(self):
        data={
            "profile_username":"user2",
            "report_reasons": "Spam",
            "description": "Spam",
        }
        reporter_profile=Profile.objects.get(username="user1")
        reported_profile=Profile.objects.get(username="user2")
        res=create_profile_report(reporter=reporter_profile, data=data)

        reported_profile2 = res.profile_id
        reporter_profile2 = res.reporter_id

        self.assertEqual(reported_profile.username, reported_profile2.username)
        self.assertEqual(reporter_profile.username, reporter_profile2.username)

