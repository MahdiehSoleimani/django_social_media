from abc import ABC
from msilib.schema import ListView
from .forms import NewCommentForm
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from pyexpat.errors import messages
from .forms import NewPostForm
from .models import Post, Reaction, Notification, Comment, Tag, Room
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class PostListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            liked = [i for i in Post.objects.all() if Reaction.objects.filter(user=self.request.user, post=i)]
            context['liked_post'] = liked
        return context


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    is_liked = Reaction.objects.filter(user=user, post=post)
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.post = post
            data.username = user
            data.save()
            return redirect('post-detail', pk=pk)
    else:
        form = NewCommentForm()
    return render(request, 'feed/post_detail.html', {'post': post, 'is_liked': is_liked, 'form': form})


@login_required
def create_post(request):
    user = request.user
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user_name = user
            data.save()
            messages.success(request, f"Posted Successfully")
            return redirect('home')
    else:
        form = NewPostForm()
    return render(request, 'feed/create_post.html', {'form': form})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['description', 'pic', 'tags']
    template_name = 'create_post.html'

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)


class UserPostListView(LoginRequiredMixin):
    """
       Displays a list of posts, ordered by the creation date.
    """
    model = Post
    template_name = 'user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self):
        context = super(UserPostListView, self).get_context_data()
        user = get_object_or_404('User', username=self.get('username'))
        for reaction in Post.objects.filter(user_name=user):
            if Reaction.objects.filter(user=self.request.user, post=reaction):
                liked = [reaction]
                context = {'liked_post': liked}
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
def search_post(request):
    query = request.GET.get('post')
    object_list = Post.objects.filter(tags_incontains=query)
    context = {'posts': object_list}
    return render(request, 'search_post', context)


class PostDetailView(LoginRequiredMixin, DetailView):
    """
    Displays the details of a specific post
    """
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allows users to create a new post
    """
    model = Post
    template_name = 'post_create.html'
    fields = ['description', 'pic', 'user', 'slug']
    success_url = reverse_lazy('post_list')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    : Allows users to delete a post.
    """
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comment_create.html'
    fields = ['comment', 'reply']
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['post_id'])
        return super().form_valid(form)


class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'tag_list.html'
    context_object_name = 'tags'


class TagDetailView(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = 'tag_detail.html'
    context_object_name = 'tag'


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'room_list.html'
    context_object_name = 'rooms'


class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = 'room_detail.html'
    context_object_name = 'room'


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notification_list.html'
    context_object_name = 'notifications'
    ordering = ['-date']
    paginate_by = 10


@login_required
def show_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user)
    context = {
        'user': user,
        'notification': notifications
    }
    return render(request, 'show_notifications', context)


class ReactionCreateView(LoginRequiredMixin, CreateView):
    model = Reaction
    template_name = 'reaction_create.html'
    fields = ['status']
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['post_id'])
        return super().form_valid(form)
