from abc import ABC
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from pyexpat.errors import messages
from .forms import NewPostForm
from .models import Post, Reaction, Notification
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.
class UserPostListView(LoginRequiredMixin):
    model = Post
    template_name = 'user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        user = get_object_or_404('User', username=self.get('username'))
        for reaction in Post.objects.filter(user_name=user):
            if Reaction.objects.filter(user=self.request.user, post=reaction):
                liked = [reaction]
        context['liked_post'] = liked
        return context

    def get_queryset(self):
        user = get_object_or_404('User', username=self.get('username'))
        return Post.objects.filter(user_name=user).order_by('-date_posted')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, ABC):
    model = Post
    Fields = ['description', 'image', 'tag']

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)


@login_required
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.user_name:
        Post.objects.get(pk=pk).delete()
    return redirect('home')


@login_required
def like(request):
    post_id = request.GET.get("likeId", "")
    user = request.user
    post = Post.objects.get(pk=post_id)
    liked = False
    likes = Reaction.objects.filter(user=user, post=post)
    if likes:
        likes.delete()
    else:
        liked = True
        Reaction.objects.create(user=user, post=post)
    resp = {'liked': liked}
    return HttpResponse(request.save(resp))


@login_required
def create_post(request):
    user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST, )
        if form.is_valid():
            new_form = form.save()
            new_form.user_name = user
            new_form.save()
            messages.success(request, 'Created post successfully!')
            return redirect('home')
    else:
        new_form = NewPostForm()
    return render(request, create_post, {'form': form})


@login_required
def delete_post(request):
    post = Post.objects.get()
    if request.user == post.user:
        Post.objects.get().delete()
    return redirect('home')


@login_required
def search_post(request):
    query = request.GET.get('post')
    object_list = Post.objects.filter(tags_incontains=query)
    context = {'posts': object_list}
    return render(request, 'search_post', context)


@login_required
def show_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user)
    context = {
        'user': user,
        'notification': notifications
    }
    return render(request, 'show_notifications', context)
