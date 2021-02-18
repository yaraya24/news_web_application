from django.db import models
from django.contrib.auth.models import AbstractUser
from news.models import NewsOrganisation, NewsArticle

class CustomUser(AbstractUser):
    news_preferences = models.ManyToManyField(NewsOrganisation)
    likes = models.ManyToManyField(NewsArticle, related_name="likes")


    

# Create your models here.
