from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model

from user_profile.models import User

import logging

logger = logging.getLogger(__name__)

UserModel = get_user_model()


class AuthorForm(forms.Form):
    email_or_username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email or Username'}),
        max_length=254
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        max_length=150,
        required=False
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        required=False
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
        max_length=150,
        required=False
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio'}),
        required=False
    )
    avatar = CloudinaryField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email address is already taken.")
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'bio', 'avatar']


class BasicSignUpForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inactive_user = None  # Store inactive user if found

    def clean_email(self):
        email = self.cleaned_data.get('email')
        logger.debug(f"Form object: {self}")
        existing_user = User.objects.filter(email=email).first()

        if existing_user:
            logger.debug(f"Found existing user: {existing_user.email} (Active: {existing_user.is_active})")
            self.inactive_user = existing_user if not existing_user.is_active else None

        return email

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(f"Username: {cleaned_data.get('username')}")
        logger.debug(f"Email: {cleaned_data.get('email')}")
        return cleaned_data


class FinalSignUpForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
        max_length=150,
        required=True
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio'}),
        required=False
    )
    avatar = CloudinaryField()

    class Meta:
        model = User
        fields = ['name', 'bio', 'avatar']


class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError('No such user')
