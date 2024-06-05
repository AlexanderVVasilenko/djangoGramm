from django import forms

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

        print(cleaned_data)
        return cleaned_data

    class Meta:
        model = User
        fields = ["email_or_username", "password"]


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "name", "bio", "avatar"]
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'required': False}),
            "email": forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': False}),
            "name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            "bio": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio', "rows": 3}),
            "avatar": forms.FileInput(attrs={'class': 'form-control-file', 'required': False})
        }
        labels = {
            "username": "Username",
            "email": "Email",
            "name": "Full",
            "bio": "Bio",
            "avatar": "Profile Picture"
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email address is already taken.")
        return email
