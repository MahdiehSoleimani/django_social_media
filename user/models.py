from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, PermissionsMixin
from django.shortcuts import redirect
from django.utils.itercompat import is_iterable
from django.utils.translation import gettext as _
from post import models
from core.models import BaseModel, TimeStampMixin
from django.contrib.auth.models import AbstractUser

# Register your models here.


class Profile(AbstractUser, PermissionsMixin):
    username = models.OnetoOnefield(
        User,
        on_delete=models.CASCADE,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")
    )

    image = models.ImageField(
        upload_to='profile_pics',
        null=True,
        blank=True,)
    is_online = models.BooleanField(default=False)
    password = models.CharField(
        _("Password"),
        max_length=12,
        help_text=_('password to login'))

    bio = models.CharField(_('Bio'),
                           max_length=255,
                           blank=True,
                           null=True)
    email = models.EmailField(_("email address"), blank=True)
    slug = AutoSlugField(populate_from='user')
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    def profile_posts(self):
        return self.objects.post.all()

    def __str__(self):
        return f'{self.username} Profile'


@property
def user_permissions(self):
    return self._user_permissions


def has_perms(self, perm_list, obj=None):
    if not is_iterable(perm_list) or isinstance(perm_list, str):
        raise ValueError("perm_list must be an iterable of permissions.")
    return all(self.has_perm(perm, obj) for perm in perm_list)


# STATUS_CHOICES = (
#    ('send', 'send'),
#   ('accepted', 'accepted')
# )


class FriendRequest(BaseModel):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,
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
        if account in self.sender.all():
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
        if friend not in self.sender.all():
            return False
