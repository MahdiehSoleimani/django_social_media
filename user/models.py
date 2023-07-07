from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, PermissionsMixin
from autoslug import AutoSlugField
from django.db.models import Manager
from django.utils.itercompat import is_iterable
from django.utils.translation import gettext as _
from post import models
from core.models import BaseModel, SoftDelete
from django.contrib.auth.models import AbstractUser

# Register your models here.


class Profile(AbstractUser, PermissionsMixin, SoftDelete):
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
                           null=True,
                           help_text='Write 255 char about yourself here.')
    email = models.EmailField(_("email address"), blank=False, null=False)
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

    class Meta:
        default_manager_name = 'objects'

    def profile_posts(self):
        return self.objects.post.all()

    def __str__(self):
        return f'{self.username} Profile'

    def get_absolute_url(self):
        return "/users/{}".format(self.slug)


class RecycleProfile(Profile):
    objects = Manager()

    class Meta:
        proxy = True


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


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self,  email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)