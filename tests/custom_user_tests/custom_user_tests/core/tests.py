from django.test import TestCase

from custom_user_tests.core.models import CustomUser


class CustomUserTestCase(TestCase):
    """Just make sure our CustomUser is working properly.
    """
    def setUp(self):
        CustomUser.objects.create_user(
            'user@example.com', 'password')

    def test_password(self):
        """Make sure our password was set.
        """
        user = CustomUser.objects.latest('date_joined')

        self.assertTrue(user.check_password('password'))

    def test_get_username(self):
        """Make sure the get_username function works.
        """
        user = CustomUser.objects.latest('date_joined')

        self.assertEqual(user.get_username(), 'user@example.com')
