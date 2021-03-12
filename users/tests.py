from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .forms import CustomUserCreationForm

class CustomUserTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            email='test@test.com',
            password='password123'
        )

        self.super_user = get_user_model().objects.create_superuser(
            username = 'admin',
            email = 'admin@email.com',
            password = 'password123'
        )
    
    def test_user_model(self):
        self.assertEqual(self.user.username, 'test')
        self.assertEqual(self.user.email, 'test@test.com')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_superuser)
    
    def test_super_user_model(self):
        self.assertEqual(self.super_user.username, 'admin')
        self.assertEqual(self.super_user.email, 'admin@email.com')
        self.assertTrue(self.super_user.is_active)
        self.assertTrue(self.super_user.is_superuser)

