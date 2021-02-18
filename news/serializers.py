from rest_framework import serializers
from .models import NewsArticle

class ArticleSerializer(serializers.ModelSerializer):
    liked_count = serializers.SerializerMethodField()

    class Meta:       
        fields = ('liked_count', 'id', 'news_organisation', 'article_address', 'heading', 'snippet', 'published_date', 'author', 'image_source', 'category')
        model = NewsArticle
        
    def get_liked_count(self, obj):
        qset = obj.likes.count()
        return qset
   