from rest_framework import serializers
from .models import NewsArticle



class ArticleSerializer(serializers.ModelSerializer):
    liked_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()

    class Meta:       
        fields = ('liked_by_user','liked_count', 'id', 'news_organisation', 'article_address', 'heading', 'snippet', 'published_date', 'author', 'image_source', 'category')
        model = NewsArticle
        
    def get_liked_count(self, obj):
        qset = obj.likes.count()
        
        return qset

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
   