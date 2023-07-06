from msilib.schema import ListView
from django.views import View
from .forms import NewCommentForm, PostUpdateForm, CommentEditForm, PostCreateForm, CommentReplyForm
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from pyexpat.errors import messages
from .models import Post, Reaction, Notification, Comment, Tag, Room
from django.contrib.auth.mixins import LoginRequiredMixin


class PostAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def setup(self, request, post_id, comment_id):
        self.this_post = get_object_or_404(Post, id=post_id)
        self.this_comment = get_object_or_404(Comment, id=comment_id)
        return super().setup(request, id)

    def dispatch(self, request, id):
        if self.this_post.user.id != request.user.id:
            return redirect("post:home")

        return super().dispatch(request, id)

    def post(self, request, post_id, comment_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = self.this_post
            reply.reply = self.this_comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'your reply submitted successfully', 'success')
        return redirect('home:post_detail', self.this_post.id, self.this_comment.id, )


class PostListView(ListView, View):
    """
    Displays a list of posts.
    """

    def get(self, request):
        posts = Post.objects.all()
        return render(
            request,
            "post: post_list.html",
            context={
                "posts": posts,
            },
        )


# class PostListView(ListView, View):
#         """
#         Displays a list of posts, ordered by the creation date.
#         """
#
#         model = Post
#         template_name = 'home.html'
#         context_object_name = 'posts'
#         ordering = ['-date_posted']
#         paginate_by = 10
#     def get_context_data(self, **kwargs):
#         context = super(PostListView, self).get_context_data(**kwargs)
#         if self.request.user.is_authenticated:
#             liked = [i for i in Post.objects.all() if Reaction.objects.filter(user=self.request.user, post=i)]
#             context['liked_post'] = liked
#         return context
#
#     def get_queryset(self):
#         user = get_object_or_404('User', username=self.get('user'))
#         return Post.objects.filter(user_name=user).order_by('-date_posted')


class PostDetailView(View):
    """
    Display detail of the post
    """

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        comments = post.comment_set.all()
        tags = post.tag_set.all()
        return render(
            request,
            "post: post_detail.html",
            context={
                "post": post,
                "comments": comments,
                'tags': tags
            },
        )


class PostUpdateView(View, LoginRequiredMixin, UpdateView):
    """
    View for updating an object, with a response rendered by a template.
    """

    def setup(self, request, id):
        self.this_post = get_object_or_404(Post, id=id)
        return super().setup(request, id)

    def dispatch(self, request, id):
        if self.this_post.user.id != request.user.id:
            return redirect("post:home")

        return super().dispatch(request, id)

    def get(self, request, id):
        form = PostUpdateForm(instance=self.this_post)
        return render(
            request,
            "post: update.html",
            context={
                "form": form,
            },
        )

    def post(self, request, id):
        form = PostUpdateForm(
            request.POST,
            request.FILES,
            instance=self.this_post,
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'you updated this post', 'success')
            return redirect("post:detail", self.this_post.id)
        return render(
            request,
            "post:update.html",
            context={
                "form": form,
            },
        )


class CommentEdit(View, LoginRequiredMixin, UpdateView):
    """
    View for updating an object, with a response rendered by a template.
    """

    def setup(self, request, id):
        self.this_comment = get_object_or_404(Comment, id=id)
        return super().setup(request, id)

    def dispatch(self, request, id):
        if self.this_comment.user.id != request.user.id:
            return redirect("post:home")

        return super().dispatch(request, id)

    def get(self, request, id):
        form = CommentEditForm(instance=self.this_comment)
        return render(
            request,
            "post:edit_comment.html",
            context={
                "form": form,
            },
        )

    def post(self, request, id):
        form = CommentEditForm(
            request.POST,
            request.FILES,
            instance=self.this_comment,
        )
        if form.is_valid():
            form.save()
            messages.success(request, f"Comment edited Successfully")
            return redirect("post:detail", self.this_comment.id)

        return render(
            request,
            "post:edit_comment.html",
            context={
                "form": form,
            },
        )


class SearchPost(LoginRequiredMixin, ListView):
    def get(self, request):
        query = request.GET.get('post')
        object_list = Post.objects.filter(tags_incontains=query)
        return render(request,
                      'search_post',
                      context={
                          'posts': object_list
                      },
                      )

    def post(self, request, *args):
        return self.get(request, *args)


class PostCreateView(LoginRequiredMixin, CreateView, View):
    """
    Allows users to create a new post
    """

    # model = Post
    # template_name = 'post_create.html'
    # fields = ['description', 'pic', 'user', 'slug']
    # success_url = reverse_lazy('post_list')

    def setup(self, request, id):
        self.this_post = get_object_or_404(Post, id=id)
        return super().setup(request, id)

    def dispatch(self, request, id):
        if self.this_post.user.id != request.user.id:
            return redirect("contents:home")

        return super().dispatch(request, id)

    def get(self, request, id):
        form = PostCreateForm(instance=self.this_post)
        return render(
            request,
            "post: create_post.html",
            context={
                "form": form,
            },
        )

    def post(self, request, id):
        form = PostCreateForm(
            request.POST,
            request.FILES,
            instance=self.this_post,
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'You created a new post!', 'success')
            return redirect("contents:detail", self.this_post.id)

        return render(
            request,
            "post: create_post.html",
            context={
                "form": form,
            },
        )


class PostDeleteView(LoginRequiredMixin, DeleteView, View):
    """
     Allows users to delete a post.
    """

    # model = Post
    # template_name = 'post_delete.html'
    # success_url = reverse_lazy('post_list')

    def setup(self, request, id):
        self.this_post = get_object_or_404(Post, id=id)
        return super().setup(request, id)

    def dispatch(self, request, id):
        if self.this_post.user.id != request.user.id:
            return redirect("contents:home")

        return super().dispatch(request, id)

    def get(self, request, id):
        post = Post.objects.filter(Post, id=id)
        post.delete()
        messages.success(request, 'post deleted successfully', 'success')
        return redirect('post:post_list')


class CommentCreateView(LoginRequiredMixin, CreateView, View):
    # model = Comment
    # template_name = 'comment_create.html'
    # fields = ['comment', 'reply']
    # success_url = reverse_lazy('post_list')
    #
    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     form.instance.post = Post.objects.get(pk=self.kwargs['post_id'])
    #     return super().form_valid(form)

    def setup(self, request, id):
        self.this_comment = get_object_or_404(Comment, id=id)
        return super().setup(request, id)

    def dispatch(self, request, id):
        if self.this_comment.user.id != request.user.id:
            return redirect("contents:home")

        return super().dispatch(request, id)

    def get(self, request, id):
        form = NewCommentForm(instance=self.this_comment)
        post = Post.objects.get(id=id)
        return render(
            request,
            "post: create_post.html",
            context={
                "form": form,
                'post': post
            },
        )

    def post(self, request, id):
        form = PostCreateForm(
            request.POST,
            request.FILES,
            instance=self.this_comment,
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'you created a new comment', 'success')
            return redirect("post:comment", self.this_comment.id)

        return render(
            request,
            "post: comments.html",
            context={
                "form": form,
            },
        )


class PostLikeView(LoginRequiredMixin, View):
    def setup(self, request, id):
        self.this_post = get_object_or_404(Post, id=id)
        return super().setup(request, id)

    def dispatch(self, request, id):
        if self.this_post.user.id != request.user.id:
            messages.error(request, 'Please login first', 'danger')
            return redirect("post:home")

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Reaction.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, 'you have already liked this post', 'danger')
        else:
            Reaction.objects.create(post=post, user=request.user)
            messages.success(request, 'you liked this post', 'success')
        return redirect('home:post_detail', post.id, post.slug)


class CommentLikeView(LoginRequiredMixin, View):

    def dispatch(self, request, id):
        self.this_comment = get_object_or_404(Comment, id=id)
        if self.this_comment.user.id != request.user.id:
            messages.error(request, 'Please login first', 'danger')
            return redirect("post:home")

    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        like = Reaction.objects.filter(comment=comment, user=request.user)
        if like.exists():
            messages.error(request, 'you have already liked this comment', 'danger')
        else:
            Reaction.objects.create(post=comment, user=request.user)
            messages.success(request, 'you liked this comment', 'success')
        return redirect('home:post_detail', comment.id)


class TagListView(LoginRequiredMixin, ListView):
    # model = Tag
    # template_name = 'tag_list.html'
    # context_object_name = 'tags'

    def get(self, request):
        tags = Tag.objects.all()
        return render(
            request,
            "Tag.html",
            context={
                "tags": tags,
            },
        )


class TagDetailView(LoginRequiredMixin, DetailView):
    # model = Tag
    # template_name = 'tag_detail.html'
    # context_object_name = 'tag'

    def get(self, request, id):
        tag = get_object_or_404(Tag, id=id)
        post = tag.post_set.all()
        return render(
            request,
            "post/Tag.html",
            context={
                "tag": tag,
                "posts": post,
            },
        )


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

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user)
        return render(
            request,
            'post: show_notification.html',
            context={
                'user': user,
                'notification': notifications
            },
        )

    def post(self, request, *args, **kwargs):
        notification_id = request.POST.get('notification_id')
        if notification_id:
            notification = Notification.objects.get(id=notification_id)
            # Process the notification based on your requirements
            notification.mark_as_read()
            return render(request,
                          'notification_list.html',
                          )
        else:
            return super.get(request, *args, **kwargs)


