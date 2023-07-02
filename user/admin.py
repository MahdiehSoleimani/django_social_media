from django.contrib import admin
from .models import Profile, FriendRequest, RecycleProfile


# admin.site.register(Profile)
# admin.site.register(FriendRequest)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_online', 'bio']
    list_filter = ['is_seen']
    search_fields = ['username', 'username']


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'is_active']
    list_filter = ['is_active']


@admin.register(RecycleProfile)
class RecycleProfile(admin.ModelAdmin):
    actions = ['recover']

    def get_queryset(self, request):
        return RecycleProfile.deleted.filter(is_deleted=True)

    @admin.action(description='recover deleted item')
    def recover(self, queryset):
        queryset.update(is_deleted=False, deleted_at=None)
