from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.conf import settings
# Register your models here.


class Profile(models.Model):
	user = models.ForeignKey(User,
								on_delete=models.CASCADE,)
	image = models.ImageField('Image',
                              default='default.png',
                              upload_to='profile_pics',
							  )
	password = models.CharField(
		max_length=12,
		verbose_name= _("password"),
		help_text=_('password to login'),
		null=False,
		blank=False,
	)
	bio = models.CharField(_('Bio'),
                           max_length=255,
                           blank=True,
						   null=True,)
    Datetime = models.DateTimeField(auto_now_add=True,)


	def __str__(self):
		return self.user.username


class FriendRequest(models.Model):
	to_user = models.ForeignKey(User,
                                related_name='follower',
                                on_delete=models.CASCADE)

	from_user = models.ForeignKey(User,
                                  related_name='following',
                                  on_delete=models.CASCADE)

	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.from_user.username, self.to_user.username
