from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


LOGIN_URL = reverse('rest_login')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class AuthenticationTests(APITestCase):
    """
    Test login and registration
    """

    def test_login_success(self):
        """Test successful login"""

        payload = {
            'email': 'test@test.com',
            'password': 'password',
            'is_active': True
        }

        create_user(**payload)

        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(res.data['code'], status.HTTP_200_OK)

    def test_login_user_inactive(self):
        """Test login user inactive"""

        payload = {
            'email': 'test@test.com',
            'password': 'password',
        }

        create_user(**payload)

        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(
            res.data['code'],
            status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    def test_login_not_exists_user(self):
        """Test login user that doesn't exist"""

        payload = {
            'email': 'test@test.com',
            'password': 'password',
        }

        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(
            res.data['code'],
            status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    def test_login_validation(self):
        """Test login failed validation"""

        payload = {
        }

        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(
            res.data['code'],
            status.HTTP_422_UNPROCESSABLE_ENTITY
        )

        payload = {
            'email': 'not an email format'
        }

        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(
            res.data['code'],
            status.HTTP_422_UNPROCESSABLE_ENTITY
        )
