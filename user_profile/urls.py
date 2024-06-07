# user_profile/urls.py

from django.urls import path

from user_profile import views

urlpatterns = [
    path("<str:my_username>", views.ProfileView.as_view(), name='my_profile'),
    path("accounts/emailsignup", views.SignUpView.as_view(), name='signup'),
    path("accounts/edit", views.ProfileEditView.as_view(), name='settings'),
    path("accounts/password/reset", views.ResetPasswordView.as_view(), name='reset_password'),
    path(
        "accounts/password/reset/confirm/<uidb64>/<token>",
        views.CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    )
]
