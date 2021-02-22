import json
from django.test import TestCase
from django.urls import reverse, resolve

from .views import HomePageView

from .models import NewsArticle, NewsOrganisation, Category
from django.contrib.auth import get_user_model, get_user
from rest_framework.test import APIClient, force_authenticate, APIRequestFactory
from .views import ArticlesList, ProfileView, ArticleDetailView, SavedArticles, SavedArticleDetail


class ArticleListTests(TestCase):
    def setUp(self):
        Users = get_user_model()
        self.test_user = Users.objects.create(
            username="test_user",
            password="Testpassword123",
            email="test@test.com",
        )
        self.test_user.save()
        self.news1 = NewsOrganisation.objects.create(
            name="news1", domain="www.news1.com"
        )
        self.news1.save()
        
        self.category = Category.objects.create(
            name='Politics'
        )
        self.category.save()

        self.article1 = NewsArticle.objects.create(
            news_organisation=self.news1,
            article_address="news1.com/article1",
            heading="test headline",
            snippet="test article as seen on test news1",
            author="journalist1",
            image_source="image.com",
            category=self.category,
        )
        self.article1.save()
        self.test_user.likes.add(self.article1)
        
       
        

        self.client = APIClient()
        self.factory = APIRequestFactory()

    
    def method_for_testing_views(self, view_to_test, endpoint):
        view = view_to_test.as_view()
        request = self.factory.get(endpoint)
        force_authenticate(request, user=self.test_user)
        response = view(request)
        response.render()
        return json.loads(response.content)

    def test_article(self):

        test_article = NewsArticle.objects.get(article_address="news1.com/article1")
        self.assertEqual(test_article.news_organisation, self.news1)
        self.assertEqual(test_article.heading, "test headline")
        self.assertEqual(test_article.snippet, "test article as seen on test news1")
        self.assertEqual(test_article.author, "journalist1")
        self.assertEqual(test_article.image_source, "image.com")
        self.assertEqual(test_article.category.name, "Politics")
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

    
    def test_profile_page_permissions(self):
        view = ProfileView.as_view()
        request = self.factory.get("/api/v1/profile")
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, 403)

        request = self.factory.get("/api/v1/profile/")
        force_authenticate(request, user=self.test_user)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_user.username)

        test_user2 = get_user_model().objects.create(
            username="django_user2",
            password="Testpassword123",
            email="test2@test.com",
        )
        request = self.factory.get("/api/v1/profile/")
        force_authenticate(request, user=test_user2)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_user2.username)
        self.assertNotContains(response, self.test_user.username)

    def test_profile_page(self):
        view = ProfileView.as_view()
        username = self.test_user.username 
        request = self.factory.get("/api/v1/profile/")
        force_authenticate(request, user=self.test_user)
        response = view(request, username=username)
        response.render()
        view_response = json.loads(response.content)
        self.assertEqual(view_response["username"], self.test_user.username)
        self.assertEqual(view_response["email"], self.test_user.email)
        self.assertEqual(len(view_response["follow_news_org"]), 0)

    def test_like_function(self):
        view = ArticleDetailView.as_view()
        request = self.factory.get("/api/v1/")
        force_authenticate(request, user=self.test_user)
        response = view(request, pk=self.article1.id)
        response.render()
        view_response = json.loads(response.content)
        self.assertEqual(view_response["liked_by_user"], True)
        self.assertEqual(view_response["liked_count"], 1)
        
        request = self.factory.patch("/api/v1/", {'like': 'Y'})
        force_authenticate(request, user=self.test_user)
        response = view(request, pk=self.article1.id)
        response.render()
        view_response = json.loads(response.content)
        self.assertEqual(view_response["liked_by_user"], False)
        self.assertEqual(view_response["liked_count"], 0)

        request = self.factory.patch("/api/v1/", {'like': 'Y'})
        force_authenticate(request, user=self.test_user)
        response = view(request, pk=self.article1.id)
        response.render()
        view_response = json.loads(response.content)
        self.assertEqual(view_response["liked_by_user"], True)
        self.assertEqual(view_response["liked_count"], 1)

    def test_save_function(self):
        view = ArticleDetailView.as_view()
        request = self.factory.get("/api/v1/")
        force_authenticate(request, user=self.test_user)
        response = view(request, pk=self.article1.id)
        response.render()
        view_response = json.loads(response.content)
        self.assertEqual(view_response["saved_by_user"], False)

        request = self.factory.patch("/api/v1/", {'save': 'Y'})
        force_authenticate(request, user=self.test_user)
        response = view(request, pk=self.article1.id)
        response.render()
        view_response = json.loads(response.content)
        self.assertEqual(view_response["saved_by_user"], True)

    def test_following_news_org(self):
        view_response = self.method_for_testing_views(ProfileView, "/api/v1/profile")
        self.assertEqual(view_response["follow_news_org"], [])
       
        request = self.factory.patch("/api/v1/profile", {self.news1.name: 'Y'})
        force_authenticate(request, user=self.test_user)
        view = ProfileView.as_view()
        response = view(request)
        response.render()
        view_response = json.loads(response.content)
        self.assertEqual(len(view_response["follow_news_org"]), 1)
        self.assertEqual(view_response["follow_news_org"][0]["name"], self.news1.name)

    def test_saved_articles_view(self):
        self.test_user.saves.add(self.article1)
        self.assertEqual(self.test_user.saves.filter(id=self.article1.id).first(), self.article1)
        view_response = self.method_for_testing_views(SavedArticles, "/api/v1/saved")
        self.assertEqual(len(view_response), 1)
        self.assertEqual(view_response[0]['id'], self.article1.id)
        self.assertEqual(view_response[0]['news_organisation'], self.news1.name)
        self.assertEqual(view_response[0]['heading'], self.article1.heading)
    
    def test_remove_saved_article_view(self):
        self.test_user.saves.add(self.article1)
        self.assertEqual(self.test_user.saves.count(), 1)
        self.assertEqual(self.test_user.saves.filter(id=self.article1.id).first(), self.article1)
        request = self.factory.delete("/api/v1/saved/del/")
        force_authenticate(request, user=self.test_user)
        view = SavedArticleDetail.as_view()
        response = view(request, pk=self.article1.id)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.test_user.saves.count(), 0)
        self.assertFalse(self.test_user.saves.filter(id=self.article1.id).first(), self.article1)

        """testind saved article view to ensure there are no saved articles"""
        view_response = self.method_for_testing_views(SavedArticles, "/api/v1/saved")
        self.assertEqual(len(view_response), 0)
        









        







