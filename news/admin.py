from django.contrib import admin
from .models import NewsOrganisation, NewsArticle

class ArticlesInLine(admin.TabularInline):
    model = NewsArticle

class NewsOrgAdmin(admin.ModelAdmin):
    inlines = [
        ArticlesInLine,
    ]
admin.site.register(NewsOrganisation, NewsOrgAdmin)