from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


GET_OR_INITIATE_USER_URL = reverse('user:get_or_initiate_user')
AUTH_USER_URL = reverse('rest_user_details')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class UserTests(APITestCase):

    def test_get_or_initiate_exist_user(self):
        """Test get user from access_token"""

        payload = {
            'email': 'test@test.com',
            'password': 'password',
            'is_active': True
        }

        user = create_user(**payload)
        self.client.force_authenticate(user=user)

        res = self.client.get(GET_OR_INITIATE_USER_URL)

        self.assertEqual(res.data['code'], status.HTTP_200_OK)

        res = self.client.get(AUTH_USER_URL)

        self.assertEqual(res.data['data']['pk'], user.id)

    def test_get_or_initiate_non_exist_user(self):
        """Test get user from access_token"""

        res = self.client.get(GET_OR_INITIATE_USER_URL)

        self.assertEqual(res.data['code'], status.HTTP_200_OK)

        res = self.client.get(AUTH_USER_URL)

        self.assertTrue('anonymous' in res.data['data']['email'])
