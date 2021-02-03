from django.test import TestCase
from django.urls import reverse, resolve

from .views import HomePageView

class HomePageTests(TestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)
        self.view = resolve('/')

    def test_homepage_static(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed('home.html')
        self.assertContains(self.response, 'Homepage')
        self.assertNotContains(self.response, 'incorrect page')
        self.assertEqual(self.view.view_name, 'home')
        self.assertEqual(
            self.view.func.__name__,
            HomePageView.as_view().__name__
        )

       

        

