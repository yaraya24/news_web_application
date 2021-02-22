from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from .models import NewsArticle

from rest_framework import generics, permissions, exceptions
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
        save_status = False
        if request.data.get('like'):
            if instance.likes.filter(id=request.user.id).first():
                like_status = True
            if like_status:
                request.user.likes.remove(instance)
                request.user.save()
            else:
                request.user.likes.add(instance)
                request.user.save()

        if request.data.get('save'):
            if instance.saves.filter(id=request.user.id).first():
                save_status = True
            if not save_status:
                request.user.saves.add(instance)
                request.user.save()

        return self.retrieve(request, *args, **kwargs)


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfilePageSerializer
    
    

    def get_object(self):
        """
        Returns the object the view is displaying.
        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        obj = get_object_or_404(get_user_model(), username=self.request.user.username)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    
