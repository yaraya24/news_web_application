from django.db import models
from django.contrib.auth.models import AbstractUser
from news.models import NewsOrganisation

class CustomUser(AbstractUser):
    news_preferences = models.ManyToManyField(NewsOrganisation)
    

# Create your models here.
