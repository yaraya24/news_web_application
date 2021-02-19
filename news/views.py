from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from .models import NewsArticle

from rest_framework import generics
from .models import NewsArticle, NewsOrganisation
from .serializers import ArticleSerializer, ProfilePageSerializer


class HomePageView(ListView):
    model = NewsArticle
    template_name = 'home.html'

class ArticlesList(generics.ListCreateAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = ArticleSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfilePageSerializer
    queryset = get_user_model().objects.all()
    lookup_field = 'username'