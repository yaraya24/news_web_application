from django.shortcuts import render
from django.views.generic import ListView
from .models import NewsArticle

class HomePageView(ListView):
    model = NewsArticle
    template_name = 'home.html'