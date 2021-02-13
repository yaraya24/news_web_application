from django.db import models

class NewsOrganisation(models.Model):
    name = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class NewsArticle(models.Model):
    news_organisation = models.ForeignKey(NewsOrganisation, on_delete=models.CASCADE)
    article_address = models.CharField(max_length=200, unique=True)
    heading = models.CharField(max_length=100)
    snippet = models.TextField()
    published_date = models.DateField()
    author = models.CharField(max_length=30, null=True)
    image_source = models.CharField(max_length=200, null=True, blank=True) 
    category = models.CharField(max_length=50, default='general', null=True)

    class Meta:
        ordering = ['published_date']
        indexes = [
            models.Index(fields=['article_address'])
        ]

    def __str__(self):
        return self.heading

