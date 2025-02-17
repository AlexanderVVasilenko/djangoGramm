import os
import django
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from feed.models import Post, Comment

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

User = get_user_model()


@pytest.mark.django_db
def test_create_comment_from_post_page(client):
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='password',
        is_active=True
    )
    client.login(username='testuser', password='password')

    post = Post.objects.create(description='Test Post', user=user)

    response = client.post(reverse('comment', kwargs={'pk': post.pk}), data={'content': 'Test Comment'},
                           HTTP_REFERER=reverse('post', kwargs={'pk': post.pk}))

    assert Comment.objects.filter(content='Test Comment', user=user, post=post).exists()

    assert response.status_code == 302
    assert response.url == reverse('post', kwargs={'pk': post.pk})


@pytest.mark.django_db
def test_create_comment_invalid_form(client):
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='password',
        is_active=True
    )
    client.login(username='testuser', password='password')

    post = Post.objects.create(description='Test Post', user=user)

    response = client.post(reverse('comment', kwargs={'pk': post.pk}), data={'content': ''},
                           HTTP_REFERER=reverse('post', kwargs={'pk': post.pk}))

    assert not Comment.objects.filter(user=user, post=post).exists()

    assert response.status_code == 200
    assert 'comment_form' in response.context
    assert response.context['comment_form'].errors
