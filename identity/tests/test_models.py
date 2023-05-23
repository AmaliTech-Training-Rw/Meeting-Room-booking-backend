from django.test import TestCase
from identity.models import MyAccountManager, Account
from rooms.models import Location


class LocationTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(city_name='Test City', country_name='Test Country')

    def test_str_representation(self):
        self.assertEqual(str(self.location), 'Test City')


class MyAccountManagerTestCase(TestCase):
    def setUp(self):
        self.manager = MyAccountManager()
        self.email = 'test@example.com'
        self.username = 'testuser'
        self.password = 'testpassword'                                
        
        # Create a Location object
        self.location = Location.objects.create(city_name='Test City', country_name='Test Country')

    def test_create_user(self):
        user = self.manager.create_user(email=self.email, username=self.username,
                                        password=self.password, location=self.location)
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.username, self.username)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = self.manager.create_superuser(email=self.email, username=self.username,
                                                  password=self.password, location=self.location)
        self.assertEqual(superuser.email, self.email)
        self.assertEqual(superuser.username, self.username)
        self.assertTrue(superuser.check_password(self.password))
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_user_required_fields(self):
        with self.assertRaises(ValueError):
            self.manager.create_user(email='', username='', password=self.password, location=self.location)

    def test_create_superuser_required_fields(self):
        with self.assertRaises(ValueError):
            self.manager.create_superuser(email='', username='', password=self.password, location=self.location)


class AccountTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(city_name='Test City', country_name='Test Country')
        self.user = Account.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword',
            location=self.location,
            )

    def test_str_representation(self):
        self.assertEqual(str(self.user), 'testuser')
