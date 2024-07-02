from django import forms
from django.contrib.auth.forms import UserCreationForm

from user_profile.models import User


class AuthorForm(forms.ModelForm):
    email_or_username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email or Username'}),
        max_length=254
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
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


class BasicSignUpForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super(BasicSignUpForm, self).save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.username = self.cleaned_data.get('username')
        if not commit:
            return user
        user.save()
        return user


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
    avatar = forms.ImageField(
        required=False
    )

    class Meta:
        model = User
        fields = ['name', 'bio', 'avatar']
