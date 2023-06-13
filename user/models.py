from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.conf import settings
# Register your models here.


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(_('Image'),
                              default='default.png',
                              upload_to='profile_pics')
	bio = models.CharField(_('Bio'),
                           max_length=255,
                           blank=True)
	friends = models.ManyToManyField("Profile", blank=True)
    Datetime = models.DateTimeField(auto_now_add=True)


def __str__(self):
		return str(self.user.username)


class FriendRequest(models.Model):
	to_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='to_user',
                                on_delete=models.CASCADE)

	from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='from_user',
                                  on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.from_user.username, self.to_user.username
