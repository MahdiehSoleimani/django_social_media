from django.db import models
from django.contrib.auth.models import User
#from django.urls import reverse
from core.models import BaseModel, TimeStampMixin


# This model is for any post that a user posts on the website.
class Post(models.Model, BaseModel, TimeStampMixin):
    description = models.CharField(max_length=255,
                                   blank=True)
    pic = models.ImageField(upload_to='path/to/img')
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    #def get_absolute_url(self):
        #return reverse('post-detail', kwargs={'pk': self.pk})

    def is_liked_by_user(self, user) -> bool:
        return self.like_set.filter(user=user).excist()

    def total_likes(self):
        return self.likes.count()

    def total_saves(self):
        return self.saves.count()


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

    def total_click(self):
        return self.likes.count()


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


class Room(models.Model, BaseModel):
    # room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User,
                               related_name='author_room',
                               on_delete=models.CASCADE)
    friend = models.ForeignKey(User,
                               related_name='friend_room',
                               on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room_id}-{self.author}-{self.friend}"


class Chat(models.Model):
    room_id = models.ForeignKey(Room,
                                on_delete=models.CASCADE,
                                related_name='chats')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='author_msg')
    friend = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='friend_msg')
    text = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    has_seen = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' %(self.id, self.date)