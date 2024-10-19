from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

# Create your tests here.
class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            "username" : "testcase",
            "email" : "testcase@example.com",
            "password" : "test123",
            "password2" : "test123"
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
class LoginLogoutTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='test123')
       
        
    def test_login(self):
        data = {
            "username" : "testuser",
            "password" : "test123"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']
    
    
    def test_logout(self):
        login_data = {
            "username": "testuser",
            "password": "test123"
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

     
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        
        logout_data = {"refresh": self.refresh_token}
        response = self.client.post(reverse('token_blacklist'), logout_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)