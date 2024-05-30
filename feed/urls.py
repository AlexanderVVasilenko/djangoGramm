from django.urls import path

from feed import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path("p/<post_id>", views.post, name='post'),
    path("<username>", views.profile, name='profile')
]
