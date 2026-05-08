from django.urls import path

from feed import views

app_name = 'feed'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path("p/<pk>", views.PostDetailView.as_view(), name='post'),
    path("p/<pk>/comment", views.CreateCommentView.as_view(), name='comment'),
    path("p/<pk>/like", views.ToggleLikeView.as_view(), name='toggle_like'),
    path('create/', views.PostCreateView.as_view(), name='create'),
]
