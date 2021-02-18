from django.db import models
from django.contrib.auth import get_user_model


class NewsOrganisation(models.Model):

    name = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)


    def __str__(self):
        return self.name

class NewsArticle(models.Model):
    news_organisation = models.ForeignKey(NewsOrganisation, on_delete=models.CASCADE, related_name='article')
    article_address = models.CharField(max_length=300, unique=True)
    heading = models.CharField(max_length=300)
    snippet = models.TextField()
    published_date = models.DateField(auto_now_add=True, blank=True)
    author = models.CharField(max_length=100, null=True)
    image_source = models.CharField(max_length=300, null=True, blank=True) 
    category = models.CharField(max_length=50, default='general', null=True)

    class Meta:
        ordering = ['published_date']
        indexes = [
            models.Index(fields=['article_address'])
        ]

    def __str__(self):
        return self.heading

