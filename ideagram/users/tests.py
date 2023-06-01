from django.test import TestCase
from ideagram.users.models import BaseUser
class BaseUserTest(TestCase):
    def setUp(self):
        BaseUser.objects.create(email="baseuserTestGmail1@gmail.com",
                                password="baseuserTestPassword1",
                                is_active=True, is_admin=False, is_email_verified=True)
        BaseUser.objects.create(email="baseuserTestGmail2@gmail.com",
                                password="baseuserTestPassword2",
                                is_active=True, is_admin=True, is_email_verified=False)
    def test_str(self):
        baseUser1 = BaseUser.objects.get(email="baseuserTestGmail1@gmail.com")
        baseUser2 = BaseUser.objects.get(email="baseuserTestGmail2@gmail.com")
        self.assertEqual(baseUser1.__str__(), "baseuserTestGmail1@gmail.com")
        self.assertEqual(baseUser2.__str__(), "baseuserTestGmail2@gmail.com")

    def test_is_staff(self):
        baseUser1 = BaseUser.objects.get(email="baseuserTestGmail1@gmail.com")
        baseUser2 = BaseUser.objects.get(email="baseuserTestGmail2@gmail.com")
        self.assertFalse(baseUser1.is_staff())
        self.assertTrue(baseUser2.is_staff())

    def test_is_user_active(self):
        baseUser1 = BaseUser.objects.get(email="baseuserTestGmail1@gmail.com")
        baseUser2 = BaseUser.objects.get(email="baseuserTestGmail2@gmail.com")
        self.assertTrue(baseUser1.is_user_active)
        self.assertFalse(baseUser2.is_user_active)
