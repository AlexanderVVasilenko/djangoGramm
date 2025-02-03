import pytest
from django.contrib.auth import get_user_model
from feed.models import Post

User = get_user_model()


@pytest.fixture
def create_users(db):
    user1 = User.objects.create_user(username='test1', password='<PASSWORD>', email='email@example.com')
    user2 = User.objects.create_user(username='test2', password='<PASSWORD>', email='email@example.comm')
    return user1, user2


@pytest.fixture
def create_post(db, create_users):
    user1, user2 = create_users
    post = Post.objects.create(user=user1, description="test caption")
    return post


def test_user_can_follow(create_users):
    user1, user2 = create_users
    user2.follow(user1)

    assert user1 in user2.following.all()
    assert user2 in user1.followers.all()


def test_user_can_unfollow(create_users):
    user1, user2 = create_users
    user2.follow(user1)
    user2.unfollow(user1)

    assert user1 not in user2.following.all()


def test_news_feeds(create_users, create_post):
    user1, user2 = create_users
    post = create_post

    user2.follow(user1)

    news_feed = Post.objects.filter(user__in=user2.following.all())
    assert post in news_feed


def test_user_can_like(create_users, create_post):
    user1, user2 = create_users
    post = create_post

    post.like_post(user1)

    assert user1.username in post.likes.values_list('user__username', flat=True)


def test_user_can_unlike(create_users, create_post):
    user1, user2 = create_users
    post = create_post

    post.like_post(user1)
    post.likes.filter(user=user1).delete()

    assert user1.username not in post.likes.values_list('user__username', flat=True)
