import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User
from users.api.serializers import LoginSerializer, RegisterSerializer


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {'email': 'testing@gmail.com', 'first_name': 'Test', 'last_name': 'User', 'password': 'testing321'}
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testing@gmail.com', first_name='Test', last_name='User', password='testing321')
        self.test_login()

    def test_login(self):
        data = {'email': self.user.email, 'password': 'testing321'}
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
