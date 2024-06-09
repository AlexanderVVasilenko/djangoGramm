# user_profile/tests.py
from django.urls import reverse
import pytest

from user_profile.models import User

@pytest.mark.django_db
def test_profile(client):
    user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
    url = reverse('profile', kwargs={'pk': user.pk})
    assert url == f'/{user.pk}'

@pytest.mark.django_db
def test_signup(client):
    url = reverse('signup')
    assert url == '/accounts/emailsignup'

@pytest.mark.django_db
def test_profile_edit(client):
    url = reverse('settings')
    assert url == '/accounts/edit'

@pytest.mark.django_db
def test_password_reset(client):
    url = reverse('reset_password')
    assert url == '/accounts/password/reset'

@pytest.mark.django_db
def test_password_reset_confirm(client):
    url = reverse('password_reset_confirm', kwargs={'uidb64': 'uid', 'token': 'token'})
    assert url == '/accounts/password/reset/confirm/uid/token'

@pytest.mark.django_db
def test_logout(client):
    url = reverse('logout')
    assert url == '/accounts/logout'
