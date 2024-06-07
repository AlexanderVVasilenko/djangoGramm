# user_profile/urls.py

from django.urls import path

from feed import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path("p/<pk>", views.PostDetailView.as_view(), name='post'),
    path("<pk>", views.ProfileView.as_view(), name='profile')
]
