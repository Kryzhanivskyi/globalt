import json

from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model


class UserAPITestCase(APITestCase):

    def test_registration(self):
        request_data = {
            "username": "test_username",
            "email": "test@localhost",
            "password": "test_psw"
        }
        response = self.client.post('/api/user/', request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), {'id': 1, 'username': 'test_username', 'email': 'test@localhost'})

    def test_get_method_not_allowed(self):
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TokenAPITestCase(APITestCase):

    def setUp(self) -> None:
        UserModel = get_user_model()
        self.user = UserModel.objects.create_user(username='test_username', email='test@localhost', password='test_psw')

    def get_tokens(self):
        request_data = {
            "username": "test_username",
            "password": "test_psw"
        }
        response = self.client.post('/api/token/', request_data)
        response_data = json.loads(response.content)
        self.access_token = response_data['access']
        self.refresh_token = response_data['refresh']

    def test_receiving_tokens(self):
        request_data = {
            "username": "test_username",
            "password": "test_psw"
        }
        response = self.client.post('/api/token/', request_data)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_data)
        self.assertIn('refresh', response_data)

    def test_refreshing_token(self):
        self.get_tokens()
        request_data = {
            "refresh": self.refresh_token
        }
        response = self.client.post('/api/token/refresh', request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostAPITestCase(APITestCase):

    def setUp(self) -> None:
        UserModel = get_user_model()
        self.user = UserModel.objects.create_user(username='test_username', email='test@localhost', password='test_psw')
        self.api_authentication()

    def api_authentication(self):
        self.get_tokens()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def get_tokens(self):
        request_data = {
            "username": "test_username",
            "password": "test_psw"
        }
        response = self.client.post('/api/token/', request_data)
        response_data = json.loads(response.content)
        self.access_token = response_data['access']
        self.refresh_token = response_data['refresh']

    def create_post(self):
        request_data = {
            "title": "test_post_title",
            "body": "test_post_body"
        }
        response = self.client.post('/api/post/', request_data)
        return response

    def test_receive_posts(self):
        response = self.client.get('/api/post/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_receive_posts_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/post/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_creation(self):
        response = self.create_post()
        response_data = json.loads(response.content)
        expected_response_data = {
            'id': 1,
            'title': 'test_post_title',
            'body': 'test_post_body',
            'author_name': 'test_username',
            'is_liked': False,
            'total_likes': 0
        }
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, expected_response_data)

    def test_post_like(self):
        response = self.create_post()
        response_data = json.loads(response.content)
        post_id = response_data['id']
        response = self.client.post(f'/api/post/{post_id}/like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_unlike(self):
        response = self.create_post()
        response_data = json.loads(response.content)
        post_id = response_data['id']
        response = self.client.post(f'/api/post/{post_id}/unlike/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)







