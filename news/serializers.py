from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import NewsArticle, NewsOrganisation, Category


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for the article for API output"""

    liked_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    saved_by_user = serializers.SerializerMethodField()
    news_organisation = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        """Fields provided to API for the News Article"""

        fields = (
            "saved_by_user",
            "liked_by_user",
            "liked_count",
            "id",
            "news_organisation",
            "article_address",
            "heading",
            "snippet",
            "published_date",
            "author",
            "image_source",
            "category",
        )
        model = NewsArticle

    def get_liked_count(self, obj):
        """Custom serializer method to return like count for an article"""
        return obj.likes.count()

    def get_liked_by_user(self, obj):
        """Custom serializer method to determine if logged in user likes a particular article"""
        request = self.context.get("request", None)
        if request:
            user = request.user
            if obj.likes.filter(id=user.id).first():
                return True
            else:
                return False
        else:
            return None

    def get_saved_by_user(self, obj):
        """Custom serializer method to determine if logged in user has saved a particular article"""
        request = self.context.get("request", None)
        if request:
            user = request.user
            if obj.saves.filter(id=user.id).first():
                return True
            else:
                return False
        else:
            return None


class ProfilePageFollowedNews(serializers.ModelSerializer):
    """Serializer to show News Organisations name instead of id for the profile endpoint"""
    class Meta:
        model = NewsOrganisation
        fields = ["name"]


class ProfilePageFollowedCategories(serializers.ModelSerializer):
    """Serializer to show Category name instead of id for the profile endpoint"""
    class Meta:
        model = Category
        fields = ["name"]


class ProfilePageSerializer(serializers.ModelSerializer):
    """Serializer for the profile page to display user details"""
    follow_category_list = serializers.SerializerMethodField()
    follow_news_org_list = serializers.SerializerMethodField()

    class Meta:
        """ Fields to be consumed by API for the user model"""
        model = get_user_model()
        fields = ("username", "email", "follow_news_org_list", "follow_category_list")

    def get_follow_category_list(self, obj):
        """ Custom serializer method that will return all followed categories for logged in user"""
        request = self.context.get("request", None)
        followed_categories = []
        if request:
            user = request.user
            for cat in user.follow_category.all():
                followed_categories.append(cat.name)
        return followed_categories

    def get_follow_news_org_list(self, obj):
        """ Custom serializer method that will return all followed news organisations for logged in user"""
        request = self.context.get("request", None)
        followed_news = []
        if request:
            user = request.user
            for org in user.follow_news_org.all():
                followed_news.append(org.name)
        return followed_news