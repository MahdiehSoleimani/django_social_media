from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
# This model is for any post that a user posts on the website.
class Post(models.Model):
	description = models.CharField(_('Description'), max_length=255, blank=True)
	image = models.ImageField(_("Image"), upload_to='category_images', null=True, blank=True)
    User_name = models.ForeignKey(_('Username'), on_delete=models.CASCADE())
    date_posted = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.description


# Comment model links a comment with the post and the user.
class Comments(models.Model):
	post = models.ForeignKey('Post', on_delete=models.CASCADE)
	username = models.ForeignKey(_(User),
                                 #related_name='details',
                                 on_delete=models.CASCADE)
	text = models.CharField(_('Text'), max_length=255)
	comment_date = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")


    def __str__(self):
        return f'comment on {self.post.name}'

# It stores the like info. It has the user who created the like and the post on which like was made.
class Like(models.Model):
	user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
	post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
