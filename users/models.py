from django.db import models
from django.contrib.auth.models import AbstractUser
from news.models import NewsOrganisation, NewsArticle, Category

class CustomUser(AbstractUser):
    follow_news_org = models.ManyToManyField(NewsOrganisation, related_name='followed_by')
    likes = models.ManyToManyField(NewsArticle, related_name="likes")
    saves = models.ManyToManyField(NewsArticle, related_name='saves')
    follow_category = models.ManyToManyField(Category, related_name="followed_by")


    
