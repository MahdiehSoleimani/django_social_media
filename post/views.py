from abc import ABC

from django.shortcuts import redirect
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Reaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
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
    response = request.save(resp)
    return HttpResponse(response)
