"""
Tests for the models of the core app.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test the core app models."""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful."""
        email = 'test@expamle.com'
        password = 'TestPass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized."""
        sample_emails = [
            ['TEST1@EXAMPLE.COM', 'TEST1@example.com'],
            ['TeSt2@ExAmPlE.cOm', 'TeSt2@example.com'],
            ['TEST.USER+ALIAS@EXAMPLE.COM', 'TEST.USER+ALIAS@example.com'],
            ['  test3@EXAMPLE.COM  ', 'test3@example.com'],
            ['TEST@SUB.EXAMPLE.COM', 'TEST@sub.example.com'],
            ['Test.User@Example.Co.Uk', 'Test.User@example.co.uk'],
            ['TEST+ALIAS@EXAMPLE.ORG', 'TEST+ALIAS@example.org'],
            ['TEST@EXAMPLE', 'TEST@example'],
            ['TEST_UŻYTKOWNIK@EXAMPLE.COM', 'TEST_UŻYTKOWNIK@example.com'],
            ['TEST-USER@EXAMPLE.COM', 'TEST-USER@example.com']
        ]

        for input_email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(
                email=input_email,
                password='test123'
            )
            self.assertEqual(user.email, expected_email)

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
