from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import BaseModel, TimeStampMixin


# This model is for any post that a user posts on the website.
class Post(models.Model, BaseModel, TimeStampMixin):
    description = models.CharField(max_length=255,
                                   blank=True)
    pic = models.ImageField(upload_to='path/to/img')
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def is_liked_by_user(self, user) -> bool:
        return self.like_set.filter(user=user).excist()


# Comment model links a comment with the post and the user.
class Comments(models.Model, BaseModel, TimeStampMixin):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)
    username = models.ForeignKey(User,
                                 related_name='details',
                                 on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    reply = models.ForeignKey('self',
                              null=True,
                              blank=True)


class Tag(models.Model, BaseModel, TimeStampMixin):
    text = models.TextField(max_length=20)
    post = models.ManyToManyField('Post',
                                  related_name='Tag')


# It stores the like info. It has the user who created the like and the post on which like was made.
class Like(models.Model, BaseModel, TimeStampMixin):
    user = models.ForeignKey(User,
                             related_name='likes',
                             on_delete=models.CASCADE)

    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)

