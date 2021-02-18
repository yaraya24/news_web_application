from django.shortcuts import render
from django.views.generic import ListView
from .models import NewsArticle

from rest_framework import generics
from .models import NewsArticle, NewsOrganisation
from .serializers import ArticleSerializer


class HomePageView(ListView):
    model = NewsArticle
    template_name = 'home.html'

class ArticlesList(generics.ListCreateAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = ArticleSerializer