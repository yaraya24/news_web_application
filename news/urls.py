from django.urls import path
from .views import ProfileView, ArticlesList

urlpatterns = [
    path('', ArticlesList.as_view(), name='home'),
    path('profile/<username>', ProfileView.as_view(), name='profile')
    
]