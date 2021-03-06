from django.urls import path
from .views import (
    ProfileView,
    ArticlesList,
    ArticleDetailView,
    SavedArticles,
    SavedArticleDetail,
    UserFeed,
    SportsView,
    BusinessView,
    CultureView,
    TechnologyView
)

urlpatterns = [
    path("", ArticlesList.as_view(), name="home"),
    path("<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("saved/", SavedArticles.as_view(), name="saved"),
    path("saved/del/<int:pk>", SavedArticleDetail.as_view(), name="del_detail"),
    path("myfeed/", UserFeed.as_view(), name="user_feed"),
    path("sports/", SportsView.as_view(), name="sports_view"),
    path("business/", BusinessView.as_view(), name="business_view"),
    path("culture/", CultureView.as_view(), name="culture_view"),
    path("technology/", TechnologyView.as_view(), name="technology_view"),
]