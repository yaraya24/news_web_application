from django.urls import path

from .views import SignupPageView, ProfilePage

urlpatterns = [
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('profile/<username>', ProfilePage.as_view(), name='profile')
]