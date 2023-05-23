from django.contrib.auth import get_user_model
from identity.backends import CaseInsensitiveModelBackend
from rooms.models import Location
from django.test import TestCase
from django.http.request import HttpRequest


class CaseInsensitiveModelBackendTest(TestCase):

    def setUp(self):
        self.backend = CaseInsensitiveModelBackend()
        self.location = Location.objects.create(city_name='Test City', country_name='Test Country')
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(username='testuser', email='test@example.com',
                                                        password='testpassword', location=self.location)

    def test_authenticate_with_correct_credentials(self):
        # Test authentication with correct credentials
        request = HttpRequest()
        user = self.backend.authenticate(request, username='testuser', password='testpassword')
        self.assertEqual(user, self.user)

    def test_authenticate_with_incorrect_credentials(self):
        # Test authentication with incorrect credentials
        request = HttpRequest()
        user = self.backend.authenticate(request, username='testuser', password='wrongpassword')
        self.assertIsNone(user)

    def test_authenticate_with_nonexistent_user(self):
        # Test authentication with a nonexistent user
        request = HttpRequest()
        user = self.backend.authenticate(request, username='nonexistentuser', password='testpassword')
        self.assertIsNone(user)

    def test_authenticate_with_case_insensitive_username(self):
        # Test authentication with a case-insensitive username
        request = HttpRequest()
        user = self.backend.authenticate(request, username='TESTUSER', password='testpassword')
        self.assertEqual(user, self.user)
