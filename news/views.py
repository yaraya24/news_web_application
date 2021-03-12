from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from .models import NewsArticle
from rest_framework.response import Response
from rest_framework import generics, permissions, exceptions, status, filters
from .models import NewsArticle, NewsOrganisation, Category
from .serializers import ArticleSerializer, ProfilePageSerializer
from .permissions import IsAuthorizedUser

class ArticlesList(generics.ListAPIView):
    """Generic ListAPI view to display all general news articles
    with no permission restrictions."""
    serializer_class = ArticleSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        """Custom queryset to retrive only News Articles that have the General category"""
        category = Category.objects.filter(name="General").first()
        return NewsArticle.objects.filter(category=category).order_by("-published_date")


class ArticleDetailView(generics.RetrieveUpdateAPIView):
    """Detailed view for a news article"""
    permission_classes = (permissions.IsAuthenticated,)
    queryset = NewsArticle.objects.all()
    serializer_class = ArticleSerializer

    def patch(self, request, *args, **kwargs):
        """Method that will update the like and save status of an article
        by the logged in user"""
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
    """Generic view that will display information about logged in user"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfilePageSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.
         
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
    """Generic view to display all saved articles by the user"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ArticleSerializer

    def get_queryset(self):
        user = self.request.user
        return user.saves.all()


class SavedArticleDetail(generics.RetrieveDestroyAPIView):
    """Class to remove articles from being saved"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ArticleSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.
        
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
    """Class to retrieve all articles based on followed categories and news orgs"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ArticleSerializer

    def get_queryset(self):
        """Custom queryset that uses union to get all articles that have categories
        and news organisations that are followed by the user"""
        user = self.request.user
        queryset = []

        news_org_query = user.follow_news_org.all()
        news_queryset = NewsArticle.objects.filter(news_organisation__in=news_org_query)

        category_query = user.follow_category.all()
        category_queryset = NewsArticle.objects.filter(category__in=category_query)

        queryset = news_queryset.union(category_queryset).order_by("-published_date")

        return queryset

class SportsView(generics.ListAPIView):
    """Generic ListAPI view to display all sports news articles"""
    serializer_class = ArticleSerializer

    def get_queryset(self):
        category = Category.objects.filter(name="Sports").first()
        return NewsArticle.objects.filter(category=category).order_by("-published_date")

class BusinessView(generics.ListAPIView):
    """Generic ListAPI view to display all business news articles"""
    serializer_class = ArticleSerializer

    def get_queryset(self):
        category = Category.objects.filter(name="Business").first()
        return NewsArticle.objects.filter(category=category).order_by("-published_date")

class CultureView(generics.ListAPIView):
    """Generic ListAPI view to display all culture news articles"""
    serializer_class = ArticleSerializer

    def get_queryset(self):
        category = Category.objects.filter(name="Culture").first()
        return NewsArticle.objects.filter(category=category).order_by("-published_date")

class TechnologyView(generics.ListAPIView):
    """Generic ListAPI view to display all technology news articles"""
    serializer_class = ArticleSerializer

    def get_queryset(self):
        category = Category.objects.filter(name="Technology").first()
        return NewsArticle.objects.filter(category=category).order_by("-published_date")

class SearchView(generics.ListAPIView):
    """Generic ListAPI view to display news articles that match the search query"""
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter,]
    search_fields = ['heading', 'snippet', 'author']
    queryset = NewsArticle.objects.all()

