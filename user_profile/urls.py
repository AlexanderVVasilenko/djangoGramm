from django.urls import path

from user_profile import views

urlpatterns = [
    path('', views.index, name='index'),
    path("<my_username>", views.my_profile, name='my_profile'),
    path("emailsignup", views.login, name='login'),
    path("<my_username>/settings", views.settings, name='settings')
]
