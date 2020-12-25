from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL_V1 = reverse('user:tokenv1')
TOKEN_URL_V2 = reverse('user:tokenv2')


def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating using with a valid payload is successful"""
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(
            user.check_password(payload['password'])
        )
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""
        payload = {
            'email': 'test@londonappdev.com',
            'name': 'test',
            'password': 'pw'
            }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    """
    These tests are using default viewset as basic couse.
    We named the login field as username (as the basic ViewSet)
    """

    def test_create_token_for_user_v1(self):
        """Test that a token is created for the user"""
        payload_create = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'name',
        }
        # self.client.post(CREATE_USER_URL, payload_create)
        create_user(**payload_create)
        payload_access = {
            'username': 'test@londonappdev.com',
            'password': 'testpass',
        }
        res = self.client.post(TOKEN_URL_V1, payload_access)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials_v1(self):
        """Test that token is not created if invalid credentials are given"""
        payload_create = {
            'email': 'test2@londonappdev.com',
            'password': 'testpass2',
            'name': 'name',
        }
        # self.client.post(CREATE_USER_URL, payload_create)
        create_user(**payload_create)
        payload_access = {
            'username': 'test2@londonappdev.com',
            'password': 'testpass',
        }
        res = self.client.post(TOKEN_URL_V1, payload_access)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_no_user_v1(self):
        """Test that token is not created if user doens't exist"""
        payload_access = {
            'username': 'test3@londonappdev.com',
            'password': 'testpass',
        }
        res = self.client.post(TOKEN_URL_V1, payload_access)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_missing_field_v1(self):
        """Test that email and password are required"""
        payload_access = {
            'username': 'test4@londonappdev.com',
        }
        res = self.client.post(TOKEN_URL_V1, payload_access)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    """
    These tests are using default viewset with customized serializer
    We named the login field as "email". This is customized on serializer
    """

    def test_create_token_for_user_v2(self):
        """Test that a token is created for the user"""
        payload_create = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'name',
        }
        create_user(**payload_create)
        payload_access = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
        }
        res = self.client.post(TOKEN_URL_V2, payload_access)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials_v2(self):
        """Test that token is not created if invalid credentials are given"""
        payload_create = {
            'email': 'test2@londonappdev.com',
            'password': 'testpass2',
            'name': 'name',
        }
        create_user(**payload_create)
        payload_access = {
            'email': 'test2@londonappdev.com',
            'password': 'testpass',
        }
        res = self.client.post(TOKEN_URL_V2, payload_access)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_no_user_v2(self):
        """Test that token is not created if user doens't exist"""
        payload_access = {
            'email': 'test3@londonappdev.com',
            'password': 'testpass',
        }
        res = self.client.post(TOKEN_URL_V2, payload_access)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_missing_field_v2(self):
        """Test that email and password are required"""
        payload_access = {
            'email': 'test4@londonappdev.com',
        }
        res = self.client.post(TOKEN_URL_V2, payload_access)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
