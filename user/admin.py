from django.contrib import admin
from .models import Profile, FriendRequest

# admin.site.register(Profile)
# admin.site.register(FriendRequest)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_online', 'bio']
    list_filter = ['is_seen']
    search_fields = ['username', 'username']


@admin.register(FriendRequest)
class FriendRequest(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'is_active']
    list_filter = ['is_active']

