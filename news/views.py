from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from .models import NewsArticle
from rest_framework.response import Response
from rest_framework import generics, permissions, exceptions, status
from .models import NewsArticle, NewsOrganisation, Category
from .serializers import ArticleSerializer, ProfilePageSerializer
from .permissions import IsAuthorizedUser


class HomePageView(ListView):
    model = NewsArticle
    template_name = "home.html"


class ArticlesList(generics.ListAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = ArticleSerializer


class ArticleDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = NewsArticle.objects.all()
    serializer_class = ArticleSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        like_status = False
        save_status = False
        if request.data.get("like"):
            if instance.likes.filter(id=request.user.id).first():
                like_status = True
            if like_status:
                request.user.likes.remove(instance)
                request.user.save()
            else:
                request.user.likes.add(instance)
                request.user.save()

        if request.data.get("save"):
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

    def patch(self, request, *args, **kwargs):
        """ Adding news org to a users following relation"""
        NewsOrgs = NewsOrganisation.objects.all()
        instance = self.get_object()  # current logged in user
        news_follow_status = False
        category_follow_status = False
        for newsorg in NewsOrgs:
            if request.data.get(newsorg.name):
                if instance.follow_news_org.filter(name=newsorg.name).first():
                    news_follow_status = True
                if news_follow_status:
                    instance.follow_news_org.remove(newsorg)
                    instance.save()
                else:
                    instance.follow_news_org.add(newsorg)
                    instance.save()

        """ Adding category to a users following relation"""
        categories = Category.objects.all()
        for category in categories:
            if request.data.get(category.name):
                if instance.follow_category.filter(name=category.name).first():
                    category_follow_status = True
                if category_follow_status:
                    instance.follow_category.remove(category)
                    instance.save()
                else:
                    instance.follow_category.add(category)
                    instance.save()
        return self.retrieve(request, *args, **kwargs)


class SavedArticles(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ArticleSerializer

    def get_queryset(self):
        user = self.request.user
        return user.saves.all()


class SavedArticleDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ArticleSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.
        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.request.user.saves.all()

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def delete(self, request, *args, **kwargs):
        try:
            user = self.request.user
            instance = self.get_object()
            user.saves.remove(instance)
            user.saves()
        except:
            return Response(
                "Saved article no longer exists", status.HTTP_204_NO_CONTENT
            )


class UserFeed(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ArticleSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = []

        news_org_query = user.follow_news_org.all()
        news_queryset = NewsArticle.objects.filter(news_organisation__in=news_org_query)

        category_query = user.follow_category.all()
        category_queryset = NewsArticle.objects.filter(category__in=category_query)

        queryset = news_queryset.union(category_queryset).order_by("-published_date")

        return queryset

class SportsView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        category = Category.objects.filter(name="Sports").first()
        return NewsArticle.objects.filter(category=category).order_by("-published_date")

class BusinessView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        category = Category.objects.filter(name="Business").first()
        return NewsArticle.objects.filter(category=category).order_by("-published_date")

class CultureView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        category = Category.objects.filter(name="Culture").first()
        return NewsArticle.objects.filter(category=category).order_by("-published_date")

class TechnologyView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        category = Category.objects.filter(name="Technology").first()
        return NewsArticle.objects.filter(category=category).order_by("-published_date")