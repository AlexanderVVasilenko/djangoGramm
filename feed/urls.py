from django.urls import path

from feed import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path("p/<pk>", views.PostDetailView.as_view(), name='post'),
    path("<pk>", views.ProfileView.as_view(), name='profile')
]
