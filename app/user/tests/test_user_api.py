"""
Test the user API endpoints
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    """Helper function to create a user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the user API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

        def test_user_with_email_exists_error(self):
            """Test creating a user that already exists fails"""
            payload = {
                'email': 'test@example.com',
                'password': 'testpass',
                'name': 'Test Name',
            }
            create_user(**payload)

            res = self.client.post(CREATE_USER_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_password_too_short_error(self):
            """Test that the password must be more than 5 characters"""
            payload = {
                'email': 'test@example.com',
                'password': 'pw',
                'name': 'Test Name',
            }
            res = self.client.post(CREATE_USER_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            user_exists = get_user_model().objects.filter(
                email=payload['email']
            ).exists()
            self.assertFalse(user_exists)

        def test_create_token_for_user(self):
            """Test that a token is created for the user"""
            payload = {
                 'email': 'test@example.com',
                'password': 'testpass',
                'name': 'Test Name',
            }
            create_user(**payload)
            res = self.client.post(TOKEN_URL, payload)
            self.assertIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_200_OK)

