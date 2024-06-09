
from django.urls import path

from feed import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path("p/<pk>", views.PostDetailView.as_view(), name='post'),
    path("p/<pk>/comment", views.CreateCommentView.as_view(), name='comment')
]
