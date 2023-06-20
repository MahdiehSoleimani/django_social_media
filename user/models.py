from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from post import models
from core.models import BaseModel, TimeStampMixin
# Register your models here.


class Profile(TimeStampMixin, BaseModel):
    username = models.OnetoOnefield(
        User,
        on_delete=models.CASCADE,
        unique=True,)

    image = models.ImageField(
        default='default.png',
        upload_to='profile_pics',
        null=True,
        blank=True)
    is_online = models.BooleanField(default=False)
    password = models.CharField(
        _("Password"),
        max_length=12,
        help_text=_('password to login'))

    bio = models.CharField(_('Bio'),
                           max_length=255,
                           blank=True,
                           null=True)
    email = models.EmailField()

    def profile_posts(self):
        return self.objects.post.all()

    def __str__(self):
        return f'{self.username} Profile'


# STATUS_CHOICES = (
#    ('send', 'send'),
#   ('accepted', 'accepted')
# )


class FriendRequest(BaseModel):
    sender = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='sender')
    receiver = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='receiver')
    is_active = models.BooleanField(blank=True,
                                    null=True,
                                    default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        receiver_friend_list = FriendRequest.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendRequest.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()

    def add_friend(self, account):
        if not account in self.sender.all():
            self.sender.add(account)
            self.save()

    def remove_friend(self, account):
        if account in self.receiver.all():
            self.receiver.remove(account)
            self.save()

    def unfriend(self, remove):
        remover_friends_list = self
        remover_friends_list.remove_friend(remove)
        friends_list = FriendRequest.objects.get(user=remove)
        friends_list.remove_friend(self.sender)

    def is_mutual_friend(self, friend):
        if not friend in self.sender.all():
            return False
