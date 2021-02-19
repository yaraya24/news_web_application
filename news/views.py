from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from .models import NewsArticle

from rest_framework import generics
from .models import NewsArticle, NewsOrganisation
from .serializers import ArticleSerializer, ProfilePageSerializer
from .permissions import IsAuthorizedUser


class HomePageView(ListView):
    model = NewsArticle
    template_name = 'home.html'

class ArticlesList(generics.ListCreateAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = ArticleSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthorizedUser,)
    serializer_class = ProfilePageSerializer
    queryset = get_user_model().objects.all()
    lookup_field = 'username'