from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from .models import NewsArticle

from rest_framework import generics, permissions
from .models import NewsArticle, NewsOrganisation
from .serializers import ArticleSerializer, ProfilePageSerializer
from .permissions import IsAuthorizedUser


class HomePageView(ListView):
    model = NewsArticle
    template_name = 'home.html'

class ArticlesList(generics.ListAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = ArticleSerializer

class ArticleDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = NewsArticle.objects.all()
    serializer_class = ArticleSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        like_status = False
        if request.data.get('like'):
            if instance.likes.filter(id=request.user.id).first():
                like_status = True
            if like_status:
                request.user.likes.remove(instance)
            else:
                request.user.likes.add(instance)
        return self.retrieve(request, *args, **kwargs)


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthorizedUser,)
    serializer_class = ProfilePageSerializer
    queryset = get_user_model().objects.all()
    lookup_field = 'username'