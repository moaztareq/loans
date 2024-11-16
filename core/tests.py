from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

# Create your tests here.


User = get_user_model()

class AuthenticationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', role='customer')

    def test_register_user(self):
        response = self.client.post('/core/register/', {
            "username": "newuser",
            "password": "newpassword",
            "role": "provider"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        response = self.client.post('/core/login/', {
            "username": "testuser",
            "password": "testpass"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)