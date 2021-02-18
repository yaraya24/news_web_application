from django.urls import path
from .views import HomePageView, ArticlesList

urlpatterns = [
    path('', ArticlesList.as_view(), name='home'),
    
]