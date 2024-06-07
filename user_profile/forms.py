from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class AuthorForm(forms.ModelForm):
    email_or_username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email or Username'}),
        max_length=254,
        label="Email or Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        email_or_username = cleaned_data.get('email_or_username')
        password = cleaned_data.get('password')

        if not email_or_username or not password:
            raise forms.ValidationError("All fields are required.")

        return cleaned_data

    class Meta:
        model = User
        fields = ["email_or_username", "password"]


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
    avatar = forms.ImageField(
        required=False
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email address is already taken.")
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'bio', 'avatar']


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'email', 'name']

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.username = self.cleaned_data.get('username')
        user.name = self.cleaned_data.get('name')
        if not commit:
            return user
        else:
            user.save()
            return user
