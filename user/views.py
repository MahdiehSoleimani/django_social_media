from Tools.demo.mcast import receiver
from django.shortcuts import render, redirect, get_object_or_404
from post.models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Profile, FriendRequest
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User


@receiver(user_logged_in)
def got_online(user):
    user.profile.is_online = True
    user.profile.save()


@receiver(user_logged_out)
def got_offline(user):
    user.profile.is_online = False
    user.profile.save()


def unfollow(request, id):
    user_profile = request.user.profile
    friend_profile = get_object_or_404(Profile, id=id)
    user_profile.friends.remove(friend_profile)
    friend_profile.friends.remove(user_profile)
    return HttpResponseRedirect('/user/{}'.format(friend_profile.slug))


@login_required
def profile_view(request, slug):
    profile = Profile.objects.filter(slug=slug).first()
    user = profile.user
    sent_friend_requests = FriendRequest.objects.filter(sender=profile.user)
    rec_friend_requests = FriendRequest.objects.filter(receiver=profile.user)
    user_posts = Post.objects.filter(user_name=user)

    friends = profile.friends.all()

    # is this user our friend
    status = 'none'
    if profile not in request.user.profile.friends.all():
        status = 'not_friend'

        # if we have sent him a friend request
        if len(FriendRequest.objects.filter(
                sender=request.user).filter(receiver=profile.user)) == 1:
            status = 'friend_request_sent'

        # if we have received a friend request
        if len(FriendRequest.objects.filter(
                sender=profile.user).filter(receiver=request.user)) == 1:
            status = 'friend_request_received'

    context = {
        'u': user,
        'button_status': status,
        'friends_list': friends,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests,
        'post_count': user_posts.count
    }

    return render(request, "user/profile.html", context)


class UserUnfollowView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['user_id'])
        if user.id != request.user.id:
            return super().dispatch(request)
        else:
            # messages.error(request, 'you cant follow/unfollow your account')
            return redirect('account:user_profile', user.id)

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = FriendRequest.objects.filter(sender=request.user, receiver=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'you unfollowed this user')
        else:
            messages.error(request, 'you are not following this user')
        return redirect('user_profile', user.id)


class UserFollowView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['user_id'])
        if user.id != request.user.id:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'you cant follow/unfollow your account', 'danger')
            return redirect('profile', user.id)

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = FriendRequest.objects.filter(sender=request.user, receiver=user)
        if relation.exists():
            messages.error(request, 'you are already following this user', 'danger')
        else:
            FriendRequest(sender=request.user, receiver=user).save()
            messages.success(request, 'you followed this user')


@login_required
def send_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest, created = FriendRequest.objects.get_or_create(
        sender=request.user,
        receiver=user)
    return HttpResponseRedirect('/users/{}'.format(user.profile.slug))


@login_required
def cancel_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(
        sender=request.user,
        receiver=user).first()
    frequest.delete()
    return HttpResponseRedirect('/user/{}'.format(user.profile.slug))


@login_required
def accept_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    if FriendRequest.objects.filter(from_user=request.user,
                                    to_user=from_user).first():
        request_rev = FriendRequest.objects.filter(from_user=request.user,
                                                   to_user=from_user).first()
        request_rev.delete()
    frequest.delete()
    return HttpResponseRedirect('/user/{}'.format(request.user.profile.slug))


@login_required
def search_users(request):
    query = request.GET.get('q')
    object_list = User.objects.filter(username__icontains=query)
    context = {'users': object_list}
    return render(request, "users/search_users.html", context)


def public_profile(request, username):
    """ Creating a public profile view """
    user = User.objects.get(username=username)
    return render(request, 'user/public_profile.html', {"public_user": user})


class ProfileListView(LoginRequiredMixin):
    """ All user profiles """
    model = Profile
    template_name = "user/profile.html"
    context_object_name = "profiles"

    def get_queryset(self, request):
        return Profile.objects.all().exclude(user=self.request.user)

