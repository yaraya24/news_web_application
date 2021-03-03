from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import NewsArticle, NewsOrganisation, Category


class ArticleSerializer(serializers.ModelSerializer):
    liked_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    saved_by_user = serializers.SerializerMethodField()
    news_organisation = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:       
        fields = ('saved_by_user','liked_by_user','liked_count', 'id', 'news_organisation', 'article_address', 'heading', 'snippet', 'published_date', 'author', 'image_source', 'category')
        model = NewsArticle
        
    def get_liked_count(self, obj):
        return obj.likes.count()


    def get_liked_by_user(self, obj):
        request = self.context.get('request', None)
        if request:
            user = request.user
            if obj.likes.filter(id=user.id).first():
                return True
            else:
                return False
        else:
            return None

    def get_saved_by_user(self, obj):
        request = self.context.get('request', None)
        if request:
            user = request.user
            if obj.saves.filter(id=user.id).first():
                return True
            else:
                return False
        else:
            return None




class ProfilePageFollowedNews(serializers.ModelSerializer):
    class Meta:
        model = NewsOrganisation
        fields = ['name']

class ProfilePageFollowedCategories(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields=['name']

class ProfilePageSerializer(serializers.ModelSerializer):
    follow_category_list = serializers.SerializerMethodField()
    follow_news_org_list = serializers.SerializerMethodField()

    

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'follow_news_org_list', 'follow_category_list')

    def get_follow_category_list(self, obj):
        request = self.context.get('request', None)
        followed_categories = []
        if request:
            user = request.user
            for cat in user.follow_category.all():
                followed_categories.append(cat.name)
        return followed_categories

    def get_follow_news_org_list(self, obj):
        request = self.context.get('request', None)
        followed_news = []
        if request:
            user = request.user 
            for org in user.follow_news_org.all():
                followed_news.append(org.name)
        return followed_news