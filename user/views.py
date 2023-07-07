from msilib.schema import ListView

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView, TemplateView
from django.http import HttpResponseRedirect
from .forms import ProfileUpdateForm
from .models import Profile, FriendRequest
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, EditUserForm


class UserRegisterView(View):
    form = UserRegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('post:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form(instance='post')
        return render(request,
                      'user:register.html',
                      {'form': form},
                      )

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'You registered successfully!', 'success')
            return redirect('post:home')
        return render(request,
                      'user:register.html',
                      {'form': form},
                      )


class UserLoginView(LoginView, View):
    form_class = UserLoginForm
    template_name = 'user:login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('post:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        self.next = request.GET.get('next')
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('post:home')
            messages.error(request, 'username or password is wrong', 'warning')
        return render(request,
                      self.template_name,
                      {'form': form},
                      )


class UserLogoutView(LoginRequiredMixin, View):
    """
    Logout user
    """

    def get(self, request):
        logout(request)
        messages.success(request, 'You logged out successfully', 'success')
        return redirect('post:home')


class EditUserView(LoginRequiredMixin, View):
    form_class = EditUserForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('post:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class(instance=request.user.user)
        return render(request,
                      'user: edit_profile.html',
                      {'form': form},
                      )

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'Profile edited successfully', 'success')
        return redirect('post:profile.html', request.user.id)


class ProfileListView(TemplateView, ListView, View):
    """
     Displays a list of profiles.
    """
    model = Profile
    template_name = 'all_profiles.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)

    def get(self, request):
        profile = Profile.objects.all().exclude(user=self.request.user)
        return render(
            request,
            "post: all_profiles.html",
            context={
                "profiles": profile,
            },
        )


class UserProfileView(LoginRequiredMixin, View):
    """
    Display profile of the user
    """

    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        posts = user.posts.all()
        relation = FriendRequest.objects.filter(sender=request.user, receiver=user)
        if relation.exists():
            is_following = True
        return render(request,
                      'account/profile.html',
                      context={'user': user,
                               'posts': posts,
                               'is_following': is_following}
                      )


# class ProfileUpdateView(LoginRequiredMixin, UpdateView):
#     """
#     Allows users to update their own profile.
#     """
#     model = Profile
#     template_name = 'profile_update.html'
#     fields = ['image', 'bio']
#     context_object_name = 'profile'
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(user=self.request.user)


# class FriendRequestCreateView(LoginRequiredMixin, CreateView):
#     """
#      Allows users to send friend requests.
#     """
#     model = FriendRequest
#     template_name = 'friendrequest.html'
#     fields = ['to_user']
#     success_url = reverse_lazy('profile-list')
#
#     def form_valid(self, form):
#         form.instance.sender = self.request.user
#         return super().form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['following'] = self.is_following()
#         return context
#     def is_following(self):
#         to_user = self.get_form().instance.receiver
#         return self.request.user.profile.friends.filter(pk=to_user.pk).exists()
#
#     def post(self, request, *args, **kwargs):
#         if 'follow' in request.POST:
#             return self.follow()
#         elif 'unfollow' in request.POST:
#             return self.unfollow()
#         return super().post(request, *args, **kwargs)
#
#     def follow(self):
#         to_user = self.get_form().instance.receiver
#         self.request.user.profile.friends.add(to_user.profile)
#         return redirect('profile-list')
#
#     def unfollow(self):
#         to_user = self.get_form().instance.receiver
#         self.request.user.profile.friends.remove(to_user.profile)
#         return redirect('profile-list')


class CancelFriendRequest(LoginRequiredMixin, View):
    def setup(self, request, id):
        self.this_profile = get_object_or_404(Profile, id=id)
        return super().setup(request, id)

    def dispatch(self, request, id):
        if self.this_profile.user.id != request.user.id:
            return redirect("post:home")

        return super().dispatch(request, id)

    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        FriendRequest.objects.filter(
            sender=request.user,
            receiver=user).delete()
        return HttpResponseRedirect('/user/{}'.format(user.profile.slug))


class UserFollowView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['user_id'])
        if user.id != request.user.id:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'you cant follow/unfollow your account', 'danger')
            return redirect('account:user_profile', user.id)

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = FriendRequest.objects.filter(sender=request.user, receiver=user)
        if relation.exists():
            messages.error(request, 'you are already following this user', 'danger')
        else:
            FriendRequest(sender=request.user, receiver=user).save()
            messages.success(request, 'you followed this user', 'success')
        return redirect('user: profile', user.id)


class UserUnfollowView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['user_id'])
        if user.id != request.user.id:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'you cant follow/unfollow your account', 'danger')
            return redirect('user:profile', user.id)

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = FriendRequest.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'you unfollowed this user', 'success')
        else:
            messages.error(request, 'you are not following this user', 'danger')
        return redirect('user:profile', user.id)


class SearchUsers(View):
    def get(self, request):
        query = request.GET.get('q')
        object_list = User.objects.filter(username__icontains=query)
        return render(request,
                      "user: search_users.html",
                      context=
                      {'users': object_list},
                      )


class ProfileUpdateView(LoginRequiredMixin, UpdateView, View):
    form_class = ProfileUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('post:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class(instance=request.user.profile,
                               initial={'email': request.user.email})
        return render(request,
                      'user: edit_profile.html',
                      {'form': form},
                      )

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'profile edited successfully', 'success')
        return redirect('user:profile', request.user.id)
