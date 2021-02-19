import json
from django.test import TestCase
from django.urls import reverse, resolve

from .views import HomePageView

from .models import NewsArticle, NewsOrganisation
from django.contrib.auth import get_user_model, get_user
from rest_framework.test import APIClient, force_authenticate, APIRequestFactory
from .views import ArticlesList, ProfileView


class ArticleListTests(TestCase):
    def setUp(self):
        Users = get_user_model()
        self.test_user = Users.objects.create(
            username="test_user",
            password="Testpassword123",
            email="test@test.com",
        )
        self.news1 = NewsOrganisation.objects.create(
            name="news1", domain="www.news1.com"
        )

        self.article1 = NewsArticle.objects.create(
            news_organisation=self.news1,
            article_address="news1.com/article1",
            heading="test headline",
            snippet="test article as seen on test news1",
            author="journalist1",
            image_source="image.com",
            category="Politics",
        )
        self.test_user.likes.add(self.article1)
        self.test_user.following.add(self.news1)

        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_article(self):

        test_article = NewsArticle.objects.get(article_address="news1.com/article1")
        self.assertEqual(test_article.news_organisation, self.news1)
        self.assertEqual(test_article.heading, "test headline")
        self.assertEqual(test_article.snippet, "test article as seen on test news1")
        self.assertEqual(test_article.author, "journalist1")
        self.assertEqual(test_article.image_source, "image.com")
        self.assertEqual(test_article.category, "Politics")
        self.assertEqual(
            test_article.likes.filter(username="test_user").first(), self.test_user
        )
        self.assertEqual(test_article.likes.count(), 1)

    def test_news_org(self):
        test_news_org = NewsOrganisation.objects.get(name="news1")
        self.assertEqual(test_news_org, self.news1)
        self.assertEqual(test_news_org.domain, "www.news1.com")
        self.assertEqual(
            test_news_org.article.filter(article_address="news1.com/article1").first(),
            self.article1,
        )

    def test_article_view(self):
        view = ArticlesList.as_view()
        request = self.factory.get("/api/v1/")
        force_authenticate(request, user=self.test_user)
        response = view(request)
        response.render()
        view_response = json.loads(response.content)
        self.assertEqual(request.user, self.test_user)
        self.assertEqual(view_response[0]["liked_by_user"], True)
        self.assertEqual(view_response[0]["liked_count"], 1)
        self.assertEqual(
            view_response[0]["article_address"], self.article1.article_address
        )
        self.assertEqual(view_response[0]["heading"], self.article1.heading)

        Users = get_user_model()
        test_user2 = Users.objects.create(
            username="test_user2",
            password="Testpassword123",
            email="test2@test.com",
        )
        force_authenticate(request, user=test_user2)
        response = view(request)
        response.render()
        view_response = json.loads(response.content)
        self.assertEqual(view_response[0]["liked_by_user"], False)
        self.assertEqual(view_response[0]["liked_count"], 1)

        test_user2.likes.add(self.article1)

        response = view(request)
        response.render()
        view_response = json.loads(response.content)
        self.assertEqual(view_response[0]["liked_by_user"], True)
        self.assertEqual(view_response[0]["liked_count"], 2)

    def test_profile_page(self):
        view = ProfileView.as_view()
        username = self.test_user.username 
        request = self.factory.get("/api/v1/profile/")
        response = view(request, username=username)
        response.render()
        view_response = json.loads(response.content)
        self.assertEqual(view_response["username"], self.test_user.username)
        self.assertEqual(view_response["email"], self.test_user.email)
        self.assertEqual(len(view_response["following"]), 1)
        self.assertEqual(view_response["following"][0]['name'], self.news1.name)




