from django.db import models
from django.contrib.auth.models import AbstractUser
from news.models import NewsOrganisation, NewsArticle

class CustomUser(AbstractUser):
    following = models.ManyToManyField(NewsOrganisation, related_name='following')
    likes = models.ManyToManyField(NewsArticle, related_name="likes")
    saves = models.ManyToManyField(NewsArticle, related_name='saves')


    
