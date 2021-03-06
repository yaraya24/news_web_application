from django.urls import path
from .views import (
    ProfileView,
    ArticlesList,
    ArticleDetailView,
    SavedArticles,
    SavedArticleDetail,
    UserFeed
)

urlpatterns = [
    path("", ArticlesList.as_view(), name="home"),
    path("<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("saved/", SavedArticles.as_view(), name="saved"),
    path("saved/del/<int:pk>", SavedArticleDetail.as_view(), name="del_detail"),
    path("myfeed/", UserFeed.as_view(), name="user_feed"),
]