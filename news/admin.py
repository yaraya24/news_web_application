from django.contrib import admin
from .models import NewsOrganisation, NewsArticle

class ArticlesInLine(admin.TabularInline):
    """Models that can be added and edited using Django Admin"""
    model = NewsArticle

class NewsOrgAdmin(admin.ModelAdmin):
    """ Allows to create articles via News Organisation in the Admin page"""
    inlines = [
        ArticlesInLine,
    ]
admin.site.register(NewsOrganisation, NewsOrgAdmin)
