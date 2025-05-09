import uuid
from cloudinary.models import CloudinaryField

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

    def like_post(self, user):
        Like.objects.create(post=self, user=user)

    def unlike_post(self, user):
        Like.objects.filter(post=self, user=user).delete()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return str(self.user) + self.content


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.post} - {self.user}"


class Photo(models.Model):
    post = models.ForeignKey(Post, related_name="photos", on_delete=models.CASCADE)
    image = CloudinaryField('image')
    index = PositiveSmallIntegerField()
