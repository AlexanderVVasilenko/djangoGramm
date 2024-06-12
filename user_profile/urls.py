from django.urls import path

from user_profile import views

urlpatterns = [
    path("<pk>", views.ProfileView.as_view(), name='profile'),
    path("accounts/emailsignup", views.SignUpView.as_view(), name='signup'),
    path("accounts/edit", views.ProfileEditView.as_view(), name='settings'),
    path("accounts/password/reset", views.ResetPasswordView.as_view(), name='reset_password'),
    path(
        "accounts/password/reset/confirm/<uidb64>/<token>",
        views.CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path('accounts/logout', views.custom_logout, name='logout'),
    path('accounts/confirmation_sent/', views.ConfirmationSentView.as_view(), name='confirmation_sent'),
    path(
        "accounts/emailsignup/confirm/<uidb64>/<token>",
        views.ConfirmEmailView.as_view(),
        name='confirm_email'
    ),
    path("accounts/emailsignup/success", views.FinalSignupView.as_view(), name='final_signup')
]
