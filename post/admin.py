from django.contrib import admin
from .models import Post, Comment, Reaction, Tag, Room, Chat, Notification, Image, RecyclePost


# admin.site.register(Post)
# admin.site.register(Comments)
# admin.site.register(Like)


# class PostTagInline(admin.TabularInline):
#    model = Tag
#    extra = 1


class PostImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['pic', 'user', 'description']
    search_fields = ['user']
    inlines = ['PostImageInline']

    @admin.action
    def published_post(self, post, Query):
        Query.Post.


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


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
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


@admin.register(RecyclePost)
class RecyclePost(admin.ModelAdmin):
    actions = ['recover']

    def get_queryset(self, request):
        return RecyclePost.deleted.filter(is_deleted=True)

    @admin.action(description='recover deleted item')
    def recover(self, queryset):
        queryset.update(is_deleted=False, deleted_at=None)