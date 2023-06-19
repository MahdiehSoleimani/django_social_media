from django.contrib import admin
from .models import Post, Comment, Like, Tag, Room, Chat, Notification, Image

# admin.site.register(Post)
# admin.site.register(Comments)
# admin.site.register(Like)


class PostTagInline(admin.TabularInline):
    model = Tag
    extra = 1


class PostCommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class PostImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['pic', 'user', 'description']
    search_fields = ['user']
    inlines = ['PostImageInline', 'PostCommentInline', 'PostTagInline']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'comment', 'reply']
    list_filter = ['user']
    search_fields = ['post']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['post', 'text']
    list_filter = ['text']
    search_fields = ['text']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']
    list_filter = ['post']
    search_fields = ['post']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['author', 'friend']
    search_fields = ['author']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['notification_type', 'sender', 'date']
    list_filter = ['is_seen']
    search_fields = ['sender']


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['autor', 'friend', 'has_seen']
    list_filter = ['has_seen']
    search_fields = ['author']
