from django.urls import path
from .views import ProfileView, ArticlesList, ArticleDetailView

urlpatterns = [
    path('', ArticlesList.as_view(), name='home'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('profile/<username>', ProfileView.as_view(), name='profile')
    
]