import uuid

from django.db import models
from django.db.models import PositiveSmallIntegerField

from user_profile.models import User


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Photo(models.Model):
    post = models.ForeignKey(Post, related_name="photos", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='djangoGramm/photos')
    index = PositiveSmallIntegerField()
