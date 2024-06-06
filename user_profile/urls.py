from django.urls import path

from user_profile import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='index'),
    path("<str:my_username>", views.ProfileView.as_view(), name='my_profile'),
    path("emailsignup", views.login, name='signup'),
    path("accounts/edit", views.ProfileEditView.as_view(), name='settings'),
    path("accounts/password/reset", views.ResetPasswordView.as_view(), name='reset_password')
]
