from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel, TimeStampMixin, SoftDelete
from django.utils.translation import gettext as _
from django.db.models import Q, Manager


class Post(TimeStampMixin, BaseModel, SoftDelete):
    description = models.CharField(max_length=255,
                                   blank=True,
                                   null=True,
                                   help_text='Required 255 characters or fewer words about post ',)
    pic = models.ImageField('Image',
                            upload_to='Post_image',
                            help_text='picture for post',)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             help_text="Select the user who authored the post.")
    slug = models.SlugField()

    class Meta:
        default_manager_name = 'objects'
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return "/users/{}".format(self.slug)

    def liked(self, user) -> bool:
        return self.Reaction_set.filter(user=user).excist()

    def total_likes(self):
        return self.Reaction.count()


# def total_saves(self):
# return self.saves.count()
class RecyclePost(Post):
    objects = Manager()

    class Meta:
        proxy = True


class Comment(TimeStampMixin, BaseModel):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,)
    user = models.ForeignKey(User,
                             related_name='Comments',
                             on_delete=models.CASCADE,
                             help_text="Select the user who posted the comment.",)
    comment = models.CharField(max_length=255,)
    reply = models.ForeignKey('self',
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True,
                              help_text='reply other comments')

    def get_replies(self):
        """"" 
        Retrieve all replies to this comment
        """""
        return Comment.objects.filter(reply=self)

    def add_reply(self, user, reply_content):
        """
        Create a new reply to this comment
        """
        reply = Comment.objects.create(post=self.post,
                                       user=user,
                                       comment=reply_content,
                                       reply=self)
        return reply

    def delete_comment(self):
        """
        Delete this comment and its replies
        """
        Comment.objects.filter(Q(pk=self.pk) | Q(reply=self)).delete()

# def total_click(self):
# return self.likes.count()


class Tag(TimeStampMixin, BaseModel):
    text = models.CharField(max_length=20,
                            help_text="Enter the name of the tag.")
    post = models.ManyToManyField('Post',
                                  related_name='Tag')

    def get_posts(self):
        """Retrieve all posts associated with this tag"""
        return self.post.all()

    def add_post(self, post):
        """Add a post to this tag"""
        self.post.add(post)

    def remove_post(self, post):
        """Remove a post from this tag"""
        self.post.remove(post)

    def get_post_count(self):
        """Get the number of posts associated with this tag"""
        return self.post.count()

    def is_used(self):
        """Check if this tag is used by any post"""
        return self.get_post_count() > 0


class Image(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    alt = models.CharField(_("Alternative Text"), max_length=100)
    product = models.ForeignKey("Product",
                                verbose_name=_("Product"),
                                on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to='products',)
    is_default = models.BooleanField(_("Is default image?"), default=False,)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return self.name


class Room(BaseModel, TimeStampMixin):
    # room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User,
                               related_name='author_room',
                               on_delete=models.CASCADE)
    friend = models.ForeignKey(User,
                               related_name='friend_room',
                               on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}-{self.author}-{self.friend}"


class Chat(TimeStampMixin, BaseModel):
    # room_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='chats')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='author_msg')
    friend = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='friend_msg')
    text = models.CharField(max_length=300)
    has_seen = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.id, self.created_at)


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        (1, 'Like'),
        (2, 'Follow'),
        (3, 'Comment'),
        (4, 'Reply'),
        (5, 'Like-Comment'),
        (6, 'Like-Reply')
    )

    post = models.ForeignKey('blog.Post',
                             on_delete=models.CASCADE,
                             related_name='notify_post',
                             blank=True,
                             null=True)
    sender = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='notify_from_user')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='notify_to_user')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=120, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s - %s - %s - %s' % (self.id, self.post, self.sender, self.user, self.notification_type)


class Reaction(models.Model):
    user = models.ForeignKey(User,
                             related_name='user',
                             on_delete=models.CASCADE)
    post = models.ForeignKey(user,
                             related_name='post',
                             verbose_name='reaction',
                             on_delete=models.CASCADE)
    status = models.BooleanField(default=None,
                                 null=True,
                                 blank=True)

    def like(self):
        """
        Set the reaction status to True (liked)
        """
        self.status = True
        self.save()

    def unlike(self):
        """
        Set the reaction status to False (unliked)
        """
        self.status = False
        self.save()

    def is_liked(self):
        """
        Check if the reaction is liked (status is True)
        """
        self.status = True
        self.save()

    def remove_reaction(self):
        """
        Remove the reaction by setting the status to None
        """
        self.status = None
        self.save()

    def update_reaction(self, new_status):
        """
        Update the reaction status to the provided value
        """
        self.status = new_status
        self.save()
