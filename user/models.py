from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from post import models
from core.models import BaseModel, TimeStampMixin
# Register your models here.


class Profile(models.Model, BaseModel, TimeStampMixin):
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE)

    image = models.ImageField(
        'Image',
        default='default.png',
        upload_to='profile_pics',
        null=True,
        blank=True)

    is_online = models.BooleanField(default=False)
    password = models.CharField(
        max_length=12,
        verbose_name="password",
        help_text=_('password to login'),
        null=False,
        blank=False,
    )
    bio = models.CharField(_('Bio'),
                           max_length=255,
                           blank=True,
                           null=True,)


def post_save_user_model_receiver(sender, instance, created):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass


    def profile_posts(self):
        return self.username.post_set.all()

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def __str__(self):
        return f'{self.user.username} Profile'


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class FriendList(models.Model):
    """""FriendList model"""""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()

    def unfriend(self, remove):
        remover_friends_list = self
        remover_friends_list.remove_friend(remove)
        friends_list = FriendList.objects.get(user=remove)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if not friend in self.friends.all():
            return False


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    is_active = models.BooleanField(blank=True, null=True, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        # update both sender and receiver friend list
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
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