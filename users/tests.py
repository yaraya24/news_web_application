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

class SignupPageTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)
        self.username = 'testuser'
        self.email = 'test@email.com'
        self.password = 'RA9123asd'


    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response,'account/signup.html')
        self.assertContains(self.response,'Sign Up')
        

    def test_signup_form(self):
        response = self.client.post(reverse('signup'), data={
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        })        
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)

        form_data = {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        }
        form = CustomUserCreationForm(form_data)
        self.assertFalse(form.is_valid())
        form_data = {
            'username': 'testuser2',
            'email': 'test2@test.com',
            'password1': self.password,
            'password2': self.password
        }
        form = CustomUserCreationForm(form_data)
        self.assertTrue(form.is_valid())
        
