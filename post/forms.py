from django import forms
from .models import Comment, Post, Tag, Notification


# class NewPostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['description', 'pic', 'tags']


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["user", "is_deleted"]


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        include = '__all__'


class CommentEditForm(forms.ModelForm):
    class Meta:
        model: Comment
        exclude = ['user']


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class NewTagForm(forms.Form):
    class Meta:
        model = Tag
        fields = ['post']


class NewNotificationForm(forms.Form):
    class Meta:
        model = Notification
        fields = ['post', 'sender', 'is_seen']
