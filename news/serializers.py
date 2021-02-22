from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import NewsArticle, NewsOrganisation


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

class ProfilePageSerializer(serializers.ModelSerializer):
    follow_news_org = ProfilePageFollowedNews(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'follow_news_org')

