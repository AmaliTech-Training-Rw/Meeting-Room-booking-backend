from django.test import TestCase
from django.contrib.auth import get_user_model
from identity.serializers import (LoginSerializer, PasswordResetSerializer,
                                  PasswordResetConfirmSerializer)
from identity.models import PasswordResetToken


class LoginSerializerTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_valid_login_data(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['user'], self.user)

    def test_invalid_login_data(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['non_field_errors'],
            ['Invalid username or password.'])


class PasswordResetSerializerTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_valid_email(self):
        data = {
            'email': 'test@example.com'
        }
        serializer = PasswordResetSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['email'], 'test@example.com')
        self.assertEqual(serializer.user, self.user)

    def test_invalid_email(self):
        data = {
            'email': 'nonexistent@example.com'
        }
        serializer = PasswordResetSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['email'],
            ['No user found with this email.'])

    def test_send_reset_email(self):
        serializer = PasswordResetSerializer()
        serializer.user = self.user
        request = None  # You can pass a mock request if needed
        serializer.send_reset_email(request)
        # Assert that the email was sent successfully (e.g., using a mocking
        # library)


class PasswordResetConfirmSerializerTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.token = PasswordResetToken.generate_token(self.user)

    def test_valid_password_reset(self):
        data = {
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }
        serializer = PasswordResetConfirmSerializer(
            data=data, context={'token': self.token})
        self.assertTrue(serializer.is_valid())
        serializer.save(token=self.token, user=self.user)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword'))
        self.assertFalse(
            PasswordResetToken.objects.filter(
                user=self.user,
                token=self.token).exists())

    def test_password_mismatch(self):
        data = {
            'password': 'newpassword',
            'confirm_password': 'mismatchedpassword'
        }
        serializer = PasswordResetConfirmSerializer(
            data=data, context={'token': self.token})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['non_field_errors'],
            ['Passwords do not match.'])
